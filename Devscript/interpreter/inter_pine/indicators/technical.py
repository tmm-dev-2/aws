import talib
import numpy as np
from typing import Any, Dict, List, Union
from scipy import stats
import pandas as pd

class TechnicalAnalysisEngine:
    def __init__(self):
        self.data = {}
        self.cache = {}
        
    def calculate_adaptive_ma(self, source, length):
        alpha = 2.0 / (length + 1)
        weights = np.exp(np.linspace(-alpha * length, 0, length))
        weights /= weights.sum()
        return np.convolve(source, weights, mode='valid')[-1]

    def calculate_time_weighted_ma(self, source, length):
        weights = np.arange(1, length + 1)
        return np.average(source[-length:], weights=weights)


    def beta(self, source1, source2, length):
        return talib.BETA(source1, source2, timeperiod=length)

    def correl(self, source1, source2, length):
        return talib.CORREL(source1, source2, timeperiod=length)

    def linearreg(self, source, length):
        return talib.LINEARREG(source, timeperiod=length)

    def linearreg_angle(self, source, length):
        return talib.LINEARREG_ANGLE(source, timeperiod=length)

    def linearreg_intercept(self, source, length):
        return talib.LINEARREG_INTERCEPT(source, timeperiod=length)

    def linearreg_slope(self, source, length):
        return talib.LINEARREG_SLOPE(source, timeperiod=length)

    def tsf(self, source, length):
        return talib.TSF(source, timeperiod=length)

    def var(self, source, length):
        return talib.VAR(source, timeperiod=length)

    def stddev(self, source, length):
        return talib.STDDEV(source, timeperiod=length)

    def ht_dcperiod(self, source):
        return talib.HT_DCPERIOD(source)

    def ht_dcphase(self, source):
        return talib.HT_DCPHASE(source)

    def ht_phasor(self, source):
        inphase, quadrature = talib.HT_PHASOR(source)
        return {'inphase': inphase, 'quadrature': quadrature}

    def ht_sine(self, source):
        sine, leadsine = talib.HT_SINE(source)
        return {'sine': sine, 'leadsine': leadsine}

    def ht_trendmode(self, source):
        return talib.HT_TRENDMODE(source)

    def obv(self, close, volume):
        return talib.OBV(close, volume)

    def ad(self, high, low, close, volume):
        return talib.AD(high, low, close, volume)

    def adosc(self, high, low, close, volume, fastperiod=3, slowperiod=10):
        return talib.ADOSC(high, low, close, volume, fastperiod=fastperiod, slowperiod=slowperiod)

    def adx(self, high, low, close, length):
        return talib.ADX(high, low, close, timeperiod=length)

    def adxr(self, high, low, close, length):
        return talib.ADXR(high, low, close, timeperiod=length)

    def aroon(self, high, low, length):
        aroondown, aroonup = talib.AROON(high, low, timeperiod=length)
        return {'down': aroondown, 'up': aroonup}

    def aroonosc(self, high, low, length):
        return talib.AROONOSC(high, low, timeperiod=length)

    def bop(self, open, high, low, close):
        return talib.BOP(open, high, low, close)

    def ichimoku(self, high, low, close, tenkan_period=9, kijun_period=26, senkou_span_b_period=52, displacement=26):
        tenkan_sen = (talib.MAX(high, timeperiod=tenkan_period) + talib.MIN(low, timeperiod=tenkan_period)) / 2
        kijun_sen = (talib.MAX(high, timeperiod=kijun_period) + talib.MIN(low, timeperiod=kijun_period)) / 2
        senkou_span_a = (tenkan_sen + kijun_sen) / 2
        senkou_span_b = (talib.MAX(high, timeperiod=senkou_span_b_period) + talib.MIN(low, timeperiod=senkou_span_b_period)) / 2
        chikou_span = np.roll(close, -displacement)

        return {
            'tenkan_sen': tenkan_sen,
            'kijun_sen': kijun_sen,
            'senkou_span_a': np.roll(senkou_span_a, displacement),
            'senkou_span_b': np.roll(senkou_span_b, displacement),
            'chikou_span': chikou_span
        }

    def calculate_supertrend(self, high, low, close, length=10, multiplier=3):
        atr = self.atr(high, low, close, length)

        upperband = ((high + low) / 2) + (multiplier * atr)
        lowerband = ((high + low) / 2) - (multiplier * atr)

        supertrend = np.zeros_like(close)
        direction = np.zeros_like(close)

        for i in range(1, len(close)):
            if close[i] > upperband[i-1]:
                direction[i] = 1
            elif close[i] < lowerband[i-1]:
                direction[i] = -1
            else:
                direction[i] = direction[i-1]

            if direction[i] == 1:
                supertrend[i] = lowerband[i]
            else:
                supertrend[i] = upperband[i]

        return {'supertrend': supertrend, 'direction': direction}

    def calculate_zigzag(self, high, low, deviation=5):
        pivots = []
        trend = 1
        last_high = high[0]
        last_low = low[0]

        for i in range(1, len(high)):
            if trend == 1:
                if high[i] > last_high:
                    last_high = high[i]
                elif low[i] < last_low * (1 - deviation/100):
                    pivots.append((i-1, last_high))
                    trend = -1
                    last_low = low[i]
            else:
                if low[i] < last_low:
                    last_low = low[i]
                elif high[i] > last_high * (1 + deviation/100):
                    pivots.append((i-1, last_low))
                    trend = 1
                    last_high = high[i]

        return {'pivots': pivots, 'trend': trend}

    def sma(self, source, length):
        return talib.SMA(source, timeperiod=length)

    def ema(self, source, length):
        return talib.EMA(source, timeperiod=length)

    def wma(self, source, length):
        return talib.WMA(source, timeperiod=length)

    def dema(self, source, length):
        return talib.DEMA(source, timeperiod=length)

    def tema(self, source, length):
        return talib.TEMA(source, timeperiod=length)

    def trima(self, source, length):
        return talib.TRIMA(source, timeperiod=length)

    def kama(self, source, length):
        return talib.KAMA(source, timeperiod=length)

    def mama(self, source, fastlimit=0.5, slowlimit=0.05):
        mama, fama = talib.MAMA(source, fastlimit=fastlimit, slowlimit=slowlimit)
        return {'mama': mama, 'fama': fama}

    def t3(self, source, length=5, vfactor=0.7):
        return talib.T3(source, timeperiod=length, vfactor=vfactor)

    def calculate_elastic_ma(self, source, length):
        alpha = 2.0 / (length + 1)
        elastic = np.zeros_like(source)
        elastic[0] = source[0]
        for i in range(1, len(source)):
            elastic[i] = alpha * source[i] + (1 - alpha) * elastic[i-1]
        return elastic[-1]

    def calculate_hull_ma(self, source, length):
        half_length = int(length/2)
        sqrt_length = int(np.sqrt(length))
        wmaf = self.wma(source, half_length)
        wmas = self.wma(source, length)
        diff = 2 * wmaf - wmas
        return self.wma(diff, sqrt_length)

    def calculate_arnaud_legoux_ma(self, source, length):
        m = 0.85
        h = length/2
        r = np.sqrt(2)
        weights = np.exp(-((np.arange(length) - h)**2)/(2*h*h*m*r))
        weights /= weights.sum()
        return np.convolve(source, weights, mode='valid')[-1]

    def calculate_mcginley_ma(self, source, length):
        mg = np.zeros_like(source)
        mg[0] = source[0]
        for i in range(1, len(source)):
            mg[i] = mg[i-1] + (source[i] - mg[i-1])/(length * np.power(source[i]/mg[i-1], 4))
        return mg[-1]

    def calculate_running_ma(self, source):
        return np.cumsum(source) / np.arange(1, len(source)+1)

    def calculate_geometric_ma(self, source, length):
        return np.exp(np.mean(np.log(source[-length:])))

    def calculate_kaufman_ma(self, source, length):
        er = np.abs(source[-1] - source[-length]) / np.sum(np.abs(np.diff(source[-length:])))
        fastest = 2.0 / (2.0 + 1)
        slowest = 2.0 / (30.0 + 1)
        sc = np.power((er * (fastest - slowest) + slowest), 2)
        return source[-1] * sc + (1 - sc) * source[-2]

    def calculate_chaikin_volatility(self, high, low, length):
        hl_range = high - low
        return (self.ema(hl_range, length) - self.ema(hl_range, length*2)) / self.ema(hl_range, length*2) * 100

    def calculate_donchian(self, high, low, length):
        upper = np.max(high[-length:])
        lower = np.min(low[-length:])
        middle = (upper + lower) / 2
        return {'upper': upper, 'middle': middle, 'lower': lower}

    def calculate_bbands_width(self, source, length, dev):
        bb = self.bbands(source, length, dev)
        return (bb['upper'] - bb['lower']) / bb['middle']

    def calculate_keltner_width(self, high, low, close, length):
        kc = self.keltner(high, low, close, length)
        return (kc['upper'] - kc['lower']) / kc['middle']

    def calculate_volatility_index(self, close, length):
        returns = np.diff(np.log(close))
        return np.std(returns[-length:]) * np.sqrt(252)

    def calculate_historical_volatility(self, close, length):
        returns = np.diff(np.log(close))
        return np.std(returns[-length:]) * np.sqrt(252)

    def calculate_parkinsons_volatility(self, high, low, length):
        hl = np.log(high/low)
        return np.sqrt(1/(4*length*np.log(2)) * np.sum(hl*hl))

    def calculate_volume_profile(self, close, volume, levels):
        price_bins = np.linspace(np.min(close), np.max(close), levels)
        vol_profile = np.zeros(levels)
        for i in range(len(close)):
            idx = np.digitize(close[i], price_bins)
            vol_profile[idx-1] += volume[i]
        return {'prices': price_bins, 'volumes': vol_profile}

    def calculate_vwap(self, close, volume):
        return np.cumsum(close * volume) / np.cumsum(volume)

    def calculate_volume_oscillator(self, volume, fast_length, slow_length):
        fast_ma = self.sma(volume, fast_length)
        slow_ma = self.sma(volume, slow_length)
        return ((fast_ma - slow_ma) / slow_ma) * 100

    def calculate_volume_ratio(self, volume, length):
        return volume[-1] / np.mean(volume[-length:])

    def calculate_nvi(self, close, volume):
        nvi = np.zeros_like(close)
        nvi[0] = 1000
        for i in range(1, len(close)):
            if volume[i] < volume[i-1]:
                nvi[i] = nvi[i-1] + ((close[i] - close[i-1])/close[i-1] * nvi[i-1])
            else:
                nvi[i] = nvi[i-1]
        return nvi

    def calculate_pvi(self, close, volume):
        pvi = np.zeros_like(close)
        pvi[0] = 1000
        for i in range(1, len(close)):
            if volume[i] > volume[i-1]:
                pvi[i] = pvi[i-1] + ((close[i] - close[i-1])/close[i-1] * pvi[i-1])
            else:
                pvi[i] = pvi[i-1]
        return pvi

    def calculate_pvt(self, close, volume):
        pvt = np.zeros_like(close)
        for i in range(1, len(close)):
            pvt[i] = pvt[i-1] + volume[i] * ((close[i] - close[i-1])/close[i-1])
        return pvt

    def calculate_volume_weighted_macd(self, close, volume, fast_length, slow_length, signal):
        vw_close = close * volume
        macd = self.ema(vw_close, fast_length) - self.ema(vw_close, slow_length)
        signal_line = self.ema(macd, signal)
        hist = macd - signal_line
        return {'macd': macd, 'signal': signal_line, 'hist': hist}

    def calculate_volume_weighted_rsi(self, close, volume, length):
        vw_close = close * volume
        delta = np.diff(vw_close)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = np.mean(gain[-length:])
        avg_loss = np.mean(loss[-length:])
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        return 100 - (100 / (1 + rs))

    def calculate_trend_strength(self, close, length):
        returns = np.diff(close[-length:])
        positive = np.sum(returns > 0)
        negative = np.sum(returns < 0)
        return (positive - negative) / length

    def calculate_trend_direction(self, close, length):
        return np.sign(close[-1] - close[-length])

    def calculate_trend_intensity(self, close, length):
        returns = np.diff(close[-length:])
        return np.abs(np.sum(returns)) / np.sum(np.abs(returns))

    def calculate_trend_score(self, close, length):
        ma = self.sma(close, length)
        std = np.std(close[-length:])
        return (close[-1] - ma[-1]) / std

    def calculate_trend_stability(self, close, length):
        returns = np.diff(close[-length:])
        direction = np.sign(returns)
        changes = np.sum(np.abs(np.diff(direction)))
        return 1 - (changes / (length-2))

    def calculate_trend_efficiency(self, close, length):
        price_move = abs(close[-1] - close[-length])
        path_length = np.sum(np.abs(np.diff(close[-length:])))
        return price_move / path_length if path_length != 0 else 0

    def calculate_trend_quality(self, close, length):
        returns = np.diff(close[-length:])
        positive = np.sum(returns > 0)
        negative = np.sum(returns < 0)
        return abs(positive - negative) / (positive + negative)

    def calculate_trend_fisher(self, high, low, length):
        mid = (high + low) / 2
        value = 0.33 * 2 * ((mid - np.min(mid[-length:])) / 
                           (np.max(mid[-length:]) - np.min(mid[-length:])) - 0.5) + 0.67 * value
        return 0.5 * np.log((1 + value)/(1 - value))

    def calculate_trend_regression(self, close, length):
        x = np.arange(length)
        slope, intercept = np.polyfit(x, close[-length:], 1)
        return {'slope': slope, 'intercept': intercept}

    def calculate_trend_correlation(self, close, length):
        x = np.arange(length)
        return np.corrcoef(x, close[-length:])[0,1]

    def identify_cycle(self, close, length):
        fft = np.fft.fft(close[-length:])
        frequencies = np.fft.fftfreq(length)
        dominant_period = 1/frequencies[np.argmax(np.abs(fft))]
        return abs(dominant_period)

    def calculate_cycle_period(self, close, length):
        return self.identify_cycle(close, length)

    def calculate_cycle_amplitude(self, close, length):
        fft = np.fft.fft(close[-length:])
        return np.max(np.abs(fft))

    def calculate_cycle_phase(self, close, length):
        fft = np.fft.fft(close[-length:])
        return np.angle(fft[np.argmax(np.abs(fft))])

    def forecast_cycle(self, close, length):
        period = self.calculate_cycle_period(close, length)
        amplitude = self.calculate_cycle_amplitude(close, length)
        phase = self.calculate_cycle_phase(close, length)
        t = len(close)
        return amplitude * np.sin(2*np.pi*t/period + phase)

    def calculate_cycle_momentum(self, close, length):
        cycle = self.identify_cycle(close, length)
        return np.diff(cycle[-length:])

    def calculate_cycle_strength(self, close, length):
        fft = np.fft.fft(close[-length:])
        dominant_amplitude = np.max(np.abs(fft))
        total_amplitude = np.sum(np.abs(fft))
        return dominant_amplitude / total_amplitude

    def calculate_covariance(self, source1, source2, length):
        return np.cov(source1[-length:], source2[-length:])[0,1]

    def calculate_pearson_correlation(self, source1, source2, length):
        return np.corrcoef(source1[-length:], source2[-length:])[0,1]
    
    def rsi(self, source, length=14):
        return talib.RSI(source, timeperiod=length)

    def stoch(self, high, low, close, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0):
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=fastk_period, slowk_period=slowk_period, slowk_matype=slowk_matype, slowd_period=slowd_period, slowd_matype=slowd_matype)
        return {'k': slowk, 'd': slowd}

    def stochf(self, high, low, close, fastk_period=14, fastd_period=3, fastd_matype=0):
        fastk, fastd = talib.STOCHF(high, low, close, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=fastd_matype)
        return {'k': fastk, 'd': fastd}

    def stochrsi(self, source, timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=0):
        fastk, fastd = talib.STOCHRSI(source, timeperiod=timeperiod, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=fastd_matype)
        return {'k': fastk, 'd': fastd}

    def macd(self, source, fastperiod=12, slowperiod=26, signalperiod=9):
        macd, signal, hist = talib.MACD(source, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        return {'macd': macd, 'signal': signal, 'hist': hist}

    def macdext(self, source, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0):
        macd, signal, hist = talib.MACDEXT(source, fastperiod=fastperiod, fastmatype=fastmatype, slowperiod=slowperiod, slowmatype=slowmatype, signalperiod=signalperiod, signalmatype=signalmatype)
        return {'macd': macd, 'signal': signal, 'hist': hist}

    def macdfix(self, source, signalperiod=9):
        macd, signal, hist = talib.MACDFIX(source, signalperiod=signalperiod)
        return {'macd': macd, 'signal': signal, 'hist': hist}

    def ppo(self, source, fastperiod=12, slowperiod=26, matype=0):
        return talib.PPO(source, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)

    def apo(self, source, fastperiod=12, slowperiod=26, matype=0):
        return talib.APO(source, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype)

    def cmo(self, source, timeperiod=14):
        return talib.CMO(source, timeperiod=timeperiod)

    def mom(self, source, timeperiod=10):
        return talib.MOM(source, timeperiod=timeperiod)

    def roc(self, source, timeperiod=10):
        return talib.ROC(source, timeperiod=timeperiod)

    def rocr(self, source, timeperiod=10):
        return talib.ROCR(source, timeperiod=timeperiod)

    def rocr100(self, source, timeperiod=10):
        return talib.ROCR100(source, timeperiod=timeperiod)

    def trix(self, source, timeperiod=30):
        return talib.TRIX(source, timeperiod=timeperiod)

    def willr(self, high, low, close, timeperiod=14):
        return talib.WILLR(high, low, close, timeperiod=timeperiod)

    def cci(self, high, low, close, timeperiod=14):
        return talib.CCI(high, low, close, timeperiod=timeperiod)

    def dmi(self, high, low, close, timeperiod=14):
        plus_di = talib.PLUS_DI(high, low, close, timeperiod=timeperiod)
        minus_di = talib.MINUS_DI(high, low, close, timeperiod=timeperiod)
        return {'plus_di': plus_di, 'minus_di': minus_di}

    def dx(self, high, low, close, timeperiod=14):
        return talib.DX(high, low, close, timeperiod=timeperiod)

    def minus_di(self, high, low, close, timeperiod=14):
        return talib.MINUS_DI(high, low, close, timeperiod=timeperiod)

    def minus_dm(self, high, low, timeperiod=14):
        return talib.MINUS_DM(high, low, timeperiod=timeperiod)

    def plus_di(self, high, low, close, timeperiod=14):
        return talib.PLUS_DI(high, low, close, timeperiod=timeperiod)

    def plus_dm(self, high, low, timeperiod=14):
        return talib.PLUS_DM(high, low, timeperiod=timeperiod)

    def mfi(self, high, low, close, volume, timeperiod=14):
        return talib.MFI(high, low, close, volume, timeperiod=timeperiod)

    def ultimate(self, high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28):
        return talib.ULTOSC(high, low, close, timeperiod1=timeperiod1, timeperiod2=timeperiod2, timeperiod3=timeperiod3)

    def bbands(self, source, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
        upper, middle, lower = talib.BBANDS(source, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
        return {'upper': upper, 'middle': middle, 'lower': lower}

    def atr(self, high, low, close, timeperiod=14):
        return talib.ATR(high, low, close, timeperiod=timeperiod)

    def natr(self, high, low, close, timeperiod=14):
        return talib.NATR(high, low, close, timeperiod=timeperiod)

    def keltner(self, high, low, close, timeperiod=20, multiplier=2):
        typical_price = (high + low + close) / 3
        atr = self.atr(high, low, close, timeperiod)
        middle = self.sma(typical_price, timeperiod)
        upper = middle + (multiplier * atr)
        lower = middle - (multiplier * atr)
        return {'upper': upper, 'middle': middle, 'lower': lower}

    def stdev(self, source, timeperiod=5, nbdev=1):
        return talib.STDDEV(source, timeperiod=timeperiod, nbdev=nbdev)

    def variance(self, source, timeperiod=5, nbdev=1):
        return talib.VAR(source, timeperiod=timeperiod, nbdev=nbdev)

    def standarddev(self, source, timeperiod=5, nbdev=1):
        return talib.STDDEV(source, timeperiod=timeperiod, nbdev=nbdev)

    def calculate_spearman_correlation(self, source1, source2, length):
        return stats.spearmanr(source1[-length:], source2[-length:])[0]

    def calculate_kendall_correlation(self, source1, source2, length):
        return stats.kendalltau(source1[-length:], source2[-length:])[0]

    def calculate_regression_quality(self, source, length):
        x = np.arange(length)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, source[-length:])
        return {'r_squared': r_value**2, 'p_value': p_value, 'std_err': std_err}

class TechnicalAnalysis:
    def __init__(self):
        self.ta_engine = TechnicalAnalysisEngine()
        
        self.functions = {
            'sma': lambda source, length: self.ta_engine.sma(source, length),
            'ema': lambda source, length: self.ta_engine.ema(source, length),
            'wma': lambda source, length: self.ta_engine.wma(source, length),
            'dema': lambda source, length: self.ta_engine.dema(source, length),
            'tema': lambda source, length: self.ta_engine.tema(source, length),
            'trima': lambda source, length: self.ta_engine.trima(source, length),
            'kama': lambda source, length: self.ta_engine.kama(source, length),
            'mama': lambda source: self.ta_engine.mama(source),
            't3': lambda source, length: self.ta_engine.t3(source, length),
            'ma_adaptive': lambda source, length: self.ta_engine.calculate_adaptive_ma(source, length),
            'ma_weighted_time': lambda source, length: self.ta_engine.calculate_time_weighted_ma(source, length),
            'ma_elastic': lambda source, length: self.ta_engine.calculate_elastic_ma(source, length),
            'ma_hull': lambda source, length: self.ta_engine.calculate_hull_ma(source, length),
            'ma_arnaud_legoux': lambda source, length: self.ta_engine.calculate_arnaud_legoux_ma(source, length),
            'ma_mcginley': lambda source, length: self.ta_engine.calculate_mcginley_ma(source, length),
            'ma_running': lambda source: self.ta_engine.calculate_running_ma(source),
            'ma_geometric': lambda source, length: self.ta_engine.calculate_geometric_ma(source, length),
            'ma_kaufman': lambda source, length: self.ta_engine.calculate_kaufman_ma(source, length),
            'rsi': lambda source, length: self.ta_engine.rsi(source, length),
            'stoch': lambda high, low, close, k_period, d_period: self.ta_engine.stoch(high, low, close, k_period, d_period),
            'stochf': lambda high, low, close, k_period: self.ta_engine.stochf(high, low, close, k_period),
            'stochrsi': lambda source, length: self.ta_engine.stochrsi(source, length),
            'macd': lambda source, fast_length, slow_length, signal: self.ta_engine.macd(source, fast_length, slow_length, signal),
            'macdext': lambda source, fast_length, slow_length, signal: self.ta_engine.macdext(source, fast_length, slow_length, signal),
            'macdfix': lambda source, signal: self.ta_engine.macdfix(source, signal),
            'ppo': lambda source, fast_length, slow_length: self.ta_engine.ppo(source, fast_length, slow_length),
            'apo': lambda source, fast_length, slow_length: self.ta_engine.apo(source, fast_length, slow_length),
            'cmo': lambda source, length: self.ta_engine.cmo(source, length),
            'mom': lambda source, length: self.ta_engine.mom(source, length),
            'roc': lambda source, length: self.ta_engine.roc(source, length),
            'rocr': lambda source, length: self.ta_engine.rocr(source, length),
            'rocr100': lambda source, length: self.ta_engine.rocr100(source, length),
            'trix': lambda source, length: self.ta_engine.trix(source, length),
            'willr': lambda high, low, close, length: self.ta_engine.willr(high, low, close, length),
            'cci': lambda high, low, close, length: self.ta_engine.cci(high, low, close, length),
            'dmi': lambda high, low, close, length: self.ta_engine.dmi(high, low, close, length),
            'dx': lambda high, low, close, length: self.ta_engine.dx(high, low, close, length),
            'minus_di': lambda high, low, close, length: self.ta_engine.minus_di(high, low, close, length),
            'minus_dm': lambda high, low, length: self.ta_engine.minus_dm(high, low, length),
            'plus_di': lambda high, low, close, length: self.ta_engine.plus_di(high, low, close, length),
            'plus_dm': lambda high, low, length: self.ta_engine.plus_dm(high, low, length),
            'mfi': lambda high, low, close, volume, length: self.ta_engine.mfi(high, low, close, volume, length),
            'ultimate': lambda high, low, close: self.ta_engine.ultimate_oscillator(high, low, close),
            'bbands': lambda source, length, dev: self.ta_engine.bbands(source, length, dev),
            'atr': lambda high, low, close, length: self.ta_engine.atr(high, low, close, length),
            'natr': lambda high, low, close, length: self.ta_engine.natr(high, low, close, length),
            'keltner': lambda high, low, close, length: self.ta_engine.keltner(high, low, close, length),
            'stdev': lambda source, length: self.ta_engine.stdev(source, length),
            'variance': lambda source, length: self.ta_engine.variance(source, length),
            'standarddev': lambda source, length: self.ta_engine.standarddev(source, length),
            'chaikin_volatility': lambda high, low, length: self.ta_engine.calculate_chaikin_volatility(high, low, length),
            'donchian': lambda high, low, length: self.ta_engine.calculate_donchian(high, low, length),
            'bbands_width': lambda source, length, dev: self.ta_engine.calculate_bbands_width(source, length, dev),
            'keltner_width': lambda high, low, close, length: self.ta_engine.calculate_keltner_width(high, low, close, length),
            'volatility_index': lambda close, length: self.ta_engine.calculate_volatility_index(close, length),
            'historical_volatility': lambda close, length: self.ta_engine.calculate_historical_volatility(close, length),
            'parkinsons_volatility': lambda high, low, length: self.ta_engine.calculate_parkinsons_volatility(high, low, length),
            'obv': lambda close, volume: self.ta_engine.obv(close, volume),
            'ad': lambda high, low, close, volume: self.ta_engine.ad(high, low, close, volume),
            'adosc': lambda high, low, close, volume, fast_length, slow_length: self.ta_engine.adosc(high, low, close, volume, fast_length, slow_length),
            'volume_profile': lambda close, volume, levels: self.ta_engine.calculate_volume_profile(close, volume, levels),
            'vwap': lambda close, volume: self.ta_engine.calculate_vwap(close, volume),
            'volume_oscillator': lambda volume, fast_length, slow_length: self.ta_engine.calculate_volume_oscillator(volume, fast_length, slow_length),
            'volume_ratio': lambda volume, length: self.ta_engine.calculate_volume_ratio(volume, length),
            'nvi': lambda close, volume: self.ta_engine.calculate_nvi(close, volume),
            'pvi': lambda close, volume: self.ta_engine.calculate_pvi(close, volume),
            'pvt': lambda close, volume: self.ta_engine.calculate_pvt(close, volume),
            'volume_weighted_macd': lambda close, volume, fast_length, slow_length, signal: self.ta_engine.calculate_volume_weighted_macd(close, volume, fast_length, slow_length, signal),
            'volume_weighted_rsi': lambda close, volume, length: self.ta_engine.calculate_volume_weighted_rsi(close, volume, length),
            'adx': lambda high, low, close, length: self.ta_engine.adx(high, low, close, length),
            'adxr': lambda high, low, close, length: self.ta_engine.adxr(high, low, close, length),
            'aroon': lambda high, low, length: self.ta_engine.aroon(high, low, length),
            'aroonosc': lambda high, low, length: self.ta_engine.aroonosc(high, low, length),
            'bop': lambda open, high, low, close: self.ta_engine.bop(open, high, low, close),
            'ichimoku': lambda high, low: self.ta_engine.ichimoku(high, low),
            'supertrend': lambda high, low, close, length, multiplier: self.ta_engine.calculate_supertrend(high, low, close, length, multiplier),
            'zigzag': lambda high, low, deviation: self.ta_engine.calculate_zigzag(high, low, deviation),
            'trend_strength': lambda close, length: self.ta_engine.calculate_trend_strength(close, length),
            'trend_direction': lambda close, length: self.ta_engine.calculate_trend_direction(close, length),
            'trend_intensity': lambda close, length: self.ta_engine.calculate_trend_intensity(close, length),
            'trend_score': lambda close, length: self.ta_engine.calculate_trend_score(close, length),
            'trend_stability': lambda close, length: self.ta_engine.calculate_trend_stability(close, length),
            'trend_efficiency': lambda close, length: self.ta_engine.calculate_trend_efficiency(close, length),
            'trend_quality': lambda close, length: self.ta_engine.calculate_trend_quality(close, length),
            'trend_fisher': lambda high, low, length: self.ta_engine.calculate_trend_fisher(high, low, length),
            'trend_regression': lambda close, length: self.ta_engine.calculate_trend_regression(close, length),
            'trend_correlation': lambda close, length: self.ta_engine.calculate_trend_correlation(close, length),
            'ht_dcperiod': lambda close: self.ta_engine.ht_dcperiod(close),
            'ht_dcphase': lambda close: self.ta_engine.ht_dcphase(close),
            'ht_phasor': lambda close: self.ta_engine.ht_phasor(close),
            'ht_sine': lambda close: self.ta_engine.ht_sine(close),
            'ht_trendmode': lambda close: self.ta_engine.ht_trendmode(close),
            'cycle_identifier': lambda close, length: self.ta_engine.identify_cycle(close, length),
            'cycle_period': lambda close, length: self.ta_engine.calculate_cycle_period(close, length),
            'cycle_amplitude': lambda close, length: self.ta_engine.calculate_cycle_amplitude(close, length),
            'cycle_phase': lambda close, length: self.ta_engine.calculate_cycle_phase(close, length),
            'cycle_forecast': lambda close, length: self.ta_engine.forecast_cycle(close, length),
            'cycle_momentum': lambda close, length: self.ta_engine.calculate_cycle_momentum(close, length),
            'cycle_strength': lambda close, length: self.ta_engine.calculate_cycle_strength(close, length),
            'beta': lambda source1, source2, length: self.ta_engine.beta(source1, source2, length),
            'correl': lambda source1, source2, length: self.ta_engine.correl(source1, source2, length),
            'linearreg': lambda source, length: self.ta_engine.linearreg(source, length),
            'linearreg_angle': lambda source, length: self.ta_engine.linearreg_angle(source, length),
            'linearreg_intercept': lambda source, length: self.ta_engine.linearreg_intercept(source, length),
            'linearreg_slope': lambda source, length: self.ta_engine.linearreg_slope(source, length),
            'stddev': lambda source, length: self.ta_engine.stddev(source, length),
            'tsf': lambda source, length: self.ta_engine.tsf(source, length),
            'var': lambda source, length: self.ta_engine.var(source, length),
            'covariance': lambda source1, source2, length: self.ta_engine.calculate_covariance(source1, source2, length),
            'pearson': lambda source1, source2, length: self.ta_engine.calculate_pearson_correlation(source1, source2, length),
            'spearman': lambda source1, source2, length: self.ta_engine.calculate_spearman_correlation(source1, source2, length),
            'kendall': lambda source1, source2, length: self.ta_engine.calculate_kendall_correlation(source1, source2, length),
            'regression_quality': lambda source, length: self.ta_engine.calculate_regression_quality(source, length)
        }

    def get_function(self, name: str):
        return self.functions.get(name)
