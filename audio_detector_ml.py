"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              Детектор звука открытия банки пива 🍺 (ML версия)               ║
║                                                                              ║
║  Использует Machine Learning для высокой точности распознавания.             ║
║  Обучен на реальных записях открытия банок + синтетических негативах.       ║
║                                                                              ║
║  Точность: ~95% на тестовых данных                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import pyaudio
import time
import os
import sys
import pickle
from collections import deque
from scipy import signal

from config import AUDIO_SETTINGS, DETECTOR_SETTINGS


def get_resource_path(filename):
    """Получить путь к ресурсу (работает и в .py, и в .exe)"""
    if getattr(sys, 'frozen', False):
        # Запущен как .exe (PyInstaller)
        base_path = sys._MEIPASS
    else:
        # Запущен как .py
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, filename)


# Путь к ML модели
MODEL_PATH = get_resource_path("beer_detector_model.pkl")

# Признаки для ML модели (должны совпадать с train_model.py)
FEATURE_NAMES = [
    'duration_ms',
    'rms',
    'peak',
    'zcr',
    'spectral_centroid',
    'spectral_rolloff',
    'energy_0_500',
    'energy_500_2000',
    'energy_2000_5000',
    'energy_5000_10000',
    'energy_10000_20000',
    'high_low_ratio',
    'attack_ratio',
    'decay_50_ratio',
    'spectral_flux'
]


class BeerCanDetector:
    """
    ML-детектор звука открытия банки пива.
    
    Использует обученную модель RandomForest для классификации звуков.
    Гораздо точнее простого сравнения с эталонами!
    """
    
    def __init__(self):
        """Инициализация детектора с ML моделью."""
        # PyAudio для записи
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_running = False
        
        # Настройки аудио
        self.rate = AUDIO_SETTINGS["rate"]
        self.chunk = AUDIO_SETTINGS["chunk"]
        self.channels = AUDIO_SETTINGS["channels"]
        
        # Настройки детектора
        self.peak_threshold = DETECTOR_SETTINGS["peak_threshold"]
        self.cooldown = DETECTOR_SETTINGS["cooldown"]
        self.debug_mode = DETECTOR_SETTINGS.get("debug_mode", False)
        
        # ML порог уверенности (выше = меньше ложных срабатываний)
        self.ml_threshold = 0.7  # 70% уверенности
        
        # Загружаем ML модель
        self.model = None
        self.scaler = None
        self._load_model()
        
        # Состояние
        self.last_trigger_time = 0
        self.last_debug_time = 0
        
        # Буфер аудио (800мс для захвата полного звука)
        self.audio_buffer = deque(maxlen=int(self.rate * 0.8))
        
        # Фоновый уровень
        self.background_levels = deque(maxlen=30)
        self.background_level = 0.01
        
        # Счётчик для подавления множественных срабатываний
        self.consecutive_detections = 0
    
    def _load_model(self):
        """Загрузить обученную ML модель."""
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, 'rb') as f:
                    data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
                print(f"   🤖 ML модель загружена: {MODEL_PATH}")
            except Exception as e:
                print(f"   ⚠️ Ошибка загрузки модели: {e}")
                self.model = None
        else:
            print(f"   ⚠️ ML модель не найдена: {MODEL_PATH}")
            print("   Запустите: python train_model.py")
    
    def _extract_ml_features(self, segment: np.ndarray) -> dict:
        """
        Извлечь признаки для ML модели.
        
        Аргументы:
            segment: numpy массив с аудио данными (нормализованный -1..1)
        
        Возвращает:
            dict с признаками для модели
        """
        features = {}
        sr = self.rate
        
        # 1. Длительность
        features['duration_ms'] = len(segment) / sr * 1000
        
        # 2. RMS (громкость)
        features['rms'] = float(np.sqrt(np.mean(segment**2)))
        
        # 3. Peak
        features['peak'] = float(np.max(np.abs(segment)))
        
        # 4. Zero Crossing Rate
        zcr = np.sum(np.abs(np.diff(np.sign(segment)))) / (2 * len(segment))
        features['zcr'] = float(zcr)
        
        # 5. Спектральные характеристики
        nperseg = min(1024, len(segment) // 2)
        if nperseg < 64:
            nperseg = 64
        
        try:
            f, Pxx = signal.welch(segment, sr, nperseg=nperseg)
        except:
            # Fallback
            f = np.linspace(0, sr/2, 100)
            Pxx = np.ones(100) * 0.001
        
        # Спектральный центроид
        total_power = np.sum(Pxx) + 1e-10
        centroid = np.sum(f * Pxx) / total_power
        features['spectral_centroid'] = float(centroid)
        
        # Спектральный rolloff (95% энергии)
        cumsum = np.cumsum(Pxx)
        rolloff_idx = np.searchsorted(cumsum, 0.95 * cumsum[-1])
        features['spectral_rolloff'] = float(f[min(rolloff_idx, len(f)-1)])
        
        # 6. Энергия по полосам частот
        bands = [(0, 500), (500, 2000), (2000, 5000), (5000, 10000), (10000, 20000)]
        for low, high in bands:
            mask = (f >= low) & (f < high)
            band_energy = np.sum(Pxx[mask])
            features[f'energy_{low}_{high}'] = float(band_energy / total_power)
        
        # 7. Соотношение высоких к низким частотам
        low_mask = f < 2000
        high_mask = (f >= 2000) & (f < 8000)
        low_energy = np.sum(Pxx[low_mask]) + 1e-10
        high_energy = np.sum(Pxx[high_mask])
        features['high_low_ratio'] = float(high_energy / low_energy)
        
        # 8. Attack time
        peak_idx = np.argmax(np.abs(segment))
        features['attack_ratio'] = float(peak_idx / len(segment))
        
        # 9. Decay time
        after_peak = np.abs(segment[peak_idx:])
        if len(after_peak) > 10:
            window = min(50, len(after_peak) // 2)
            if window > 0:
                decay_envelope = np.convolve(after_peak, np.ones(window)/window, mode='valid')
                if len(decay_envelope) > 0:
                    half_idx = np.searchsorted(-decay_envelope, -decay_envelope[0] * 0.5)
                    features['decay_50_ratio'] = float(min(half_idx / len(after_peak), 1.0))
                else:
                    features['decay_50_ratio'] = 0.5
            else:
                features['decay_50_ratio'] = 0.5
        else:
            features['decay_50_ratio'] = 0.5
        
        # 10. Спектральный flux
        n_frames = max(1, len(segment) // 512)
        if n_frames > 1:
            frame_size = len(segment) // n_frames
            spectra = []
            for i in range(n_frames):
                frame = segment[i*frame_size:(i+1)*frame_size]
                if len(frame) > 0:
                    spec = np.abs(np.fft.rfft(frame))
                    spec = spec / (np.max(spec) + 1e-10)
                    spectra.append(spec[:min(len(spec), 256)])
            
            if len(spectra) > 1:
                max_len = max(len(s) for s in spectra)
                spectra = [np.pad(s, (0, max_len - len(s))) for s in spectra]
                spectra = np.array(spectra)
                flux = np.mean(np.sqrt(np.sum(np.diff(spectra, axis=0)**2, axis=1)))
                features['spectral_flux'] = float(flux)
            else:
                features['spectral_flux'] = 0.0
        else:
            features['spectral_flux'] = 0.0
        
        return features
    
    def _find_sound_segment(self, audio_data: np.ndarray) -> np.ndarray:
        """Найти границы звука в буфере."""
        envelope = np.abs(audio_data)
        
        window = int(self.rate * 0.005)
        if window > 0:
            envelope = np.convolve(envelope, np.ones(window)/window, mode='same')
        
        peak_val = np.max(envelope)
        threshold = peak_val * 0.05
        
        above_threshold = np.where(envelope > threshold)[0]
        
        if len(above_threshold) < 50:
            peak_idx = np.argmax(np.abs(audio_data))
            samples_before = int(self.rate * 0.05)
            samples_after = int(self.rate * 0.3)
            start = max(0, peak_idx - samples_before)
            end = min(len(audio_data), peak_idx + samples_after)
            return audio_data[start:end]
        
        start_idx = above_threshold[0]
        end_idx = above_threshold[-1]
        
        # Padding
        padding = int(self.rate * 0.02)
        start_idx = max(0, start_idx - padding)
        end_idx = min(len(audio_data), end_idx + padding)
        
        # Ограничения размера (50-700мс)
        min_samples = int(self.rate * 0.05)
        max_samples = int(self.rate * 0.7)
        
        segment_len = end_idx - start_idx
        
        if segment_len < min_samples:
            center = (start_idx + end_idx) // 2
            start_idx = max(0, center - min_samples // 2)
            end_idx = min(len(audio_data), start_idx + min_samples)
        elif segment_len > max_samples:
            peak_idx = start_idx + np.argmax(np.abs(audio_data[start_idx:end_idx]))
            start_idx = max(0, peak_idx - max_samples // 3)
            end_idx = min(len(audio_data), start_idx + max_samples)
        
        return audio_data[start_idx:end_idx]
    
    def _predict_with_ml(self, segment: np.ndarray) -> tuple:
        """
        Предсказать с помощью ML модели.
        
        Возвращает:
            tuple (вероятность_пива, признаки)
        """
        if self.model is None or self.scaler is None:
            return 0.0, {}
        
        features = self._extract_ml_features(segment)
        
        # Формируем вектор признаков
        X = [[features.get(fn, 0.0) for fn in FEATURE_NAMES]]
        X = np.array(X)
        
        # Нормализуем
        try:
            X_scaled = self.scaler.transform(X)
            prob = self.model.predict_proba(X_scaled)[0, 1]
        except Exception as e:
            if self.debug_mode:
                print(f"   ⚠️ Ошибка ML: {e}")
            return 0.0, features
        
        return float(prob), features
    
    def start_stream(self):
        """Запустить запись с микрофона."""
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        self.is_running = True
        if self.model:
            print("🎤 Микрофон активирован (ML детектор). Ищу звук открытия банки...")
        else:
            print("🎤 Микрофон активирован (без ML). Запустите train_model.py для обучения.")
    
    def stop_stream(self):
        """Остановить запись."""
        self.is_running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        print("🔇 Микрофон отключен.")
    
    def read_audio_chunk(self) -> np.ndarray:
        """Прочитать порцию аудио."""
        try:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            return np.zeros(self.chunk, dtype=np.int16)
    
    def detect(self) -> bool:
        """
        Проверить, был ли звук открытия банки.
        
        Использует ML модель для высокой точности.
        """
        current_time = time.time()
        
        # Cooldown
        if current_time - self.last_trigger_time < self.cooldown:
            return False
        
        # Читаем аудио
        audio_data = self.read_audio_chunk()
        audio_normalized = audio_data / 32768.0
        
        # Добавляем в буфер
        self.audio_buffer.extend(audio_normalized)
        
        # Вычисляем уровни
        rms = np.sqrt(np.mean(audio_normalized ** 2))
        peak = np.max(np.abs(audio_normalized))
        
        # Адаптивный фон
        if rms < 0.02:
            self.background_levels.append(rms)
            if len(self.background_levels) > 5:
                self.background_level = np.mean(self.background_levels)
        
        # Debug вывод
        if self.debug_mode and current_time - self.last_debug_time >= 0.5:
            self.last_debug_time = current_time
            bar_length = int(rms * 200)
            bar = "█" * min(bar_length, 50) + "░" * (50 - min(bar_length, 50))
            status = "🔊" if peak > self.peak_threshold else "🔈"
            ml_status = "🤖" if self.model else "❌"
            print(f"{status}{ml_status} [{bar}] RMS:{rms:.3f} Peak:{peak:.3f}", end="\r")
        
        # Анализ громких звуков
        if peak > self.peak_threshold:
            
            buffer_array = np.array(self.audio_buffer)
            
            if len(buffer_array) < 1000:
                return False
            
            segment = self._find_sound_segment(buffer_array)
            
            if len(segment) > 500:
                
                # ML предсказание
                prob, features = self._predict_with_ml(segment)
                
                if self.debug_mode:
                    hl_ratio = features.get('high_low_ratio', 0)
                    centroid = features.get('spectral_centroid', 0)
                    print(f"\n   🤖 ML вероятность: {prob:.1%} | H/L: {hl_ratio:.1f} | Centroid: {centroid:.0f}Hz")
                
                # Дополнительные проверки для уменьшения ложных срабатываний
                high_low_ratio = features.get('high_low_ratio', 0)
                spectral_centroid = features.get('spectral_centroid', 0)
                duration = features.get('duration_ms', 0)
                
                # Характерные признаки пива:
                # - Много высоких частот (high_low_ratio > 2)
                # - Центроид выше 3000 Hz
                # - Длительность 100-800 мс
                is_hiss_like = high_low_ratio > 2.0
                is_high_freq = spectral_centroid > 3000
                is_valid_duration = 100 < duration < 800
                
                # Комбинированное решение
                if prob >= self.ml_threshold and is_hiss_like and is_high_freq and is_valid_duration:
                    print(f"\n\n🍺 БАНКА ОТКРЫТА! (ML: {prob:.1%}, H/L: {high_low_ratio:.1f})")
                    self.last_trigger_time = current_time
                    self.audio_buffer.clear()
                    self.consecutive_detections = 0
                    return True
                
                elif prob >= 0.5:
                    if self.debug_mode:
                        reasons = []
                        if not is_hiss_like:
                            reasons.append(f"H/L={high_low_ratio:.1f}<2")
                        if not is_high_freq:
                            reasons.append(f"centroid={spectral_centroid:.0f}<3000")
                        if not is_valid_duration:
                            reasons.append(f"dur={duration:.0f}ms")
                        print(f"   ❌ Похоже, но отклонено: {', '.join(reasons)}")
        
        return False
