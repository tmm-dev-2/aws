import re
from typing import Any, Dict, List, Optional, Tuple, Union
import math
import numpy as np


"""-----------------------------------------------------------------------------------------------------------------------------------------"""

#innitialization and configuration

class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current_position = 0

    def tokenize(self):
        tokens = []
        while self.current_position < len(self.source_code):
            char = self.source_code[self.current_position]
            
            if char.isspace():
                self.current_position += 1
                continue
            
            elif char.isdigit() or (char == '-' and self.peek().isdigit()):
                match = re.match(r'-?\d+(\.\d*)?', self.source_code[self.current_position:])
                if match:
                    value = float(match.group(0))
                    tokens.append(('NUMBER', value))
                    self.current_position += match.end()
                    continue
            
            elif char.isalpha():
                match = re.match(r'[a-zA-Z_]+', self.source_code[self.current_position:])
                if match:
                    identifier = match.group(0)
                    if identifier in ['andOp', 'enumType', 'exportFunc', 'forLoop', 'forInLoop', 'ifCond', 'importFunc', 'methodFunc', 'notOp', 'orOp', 'switchCase', 'typeDef', 'let', 'letip', 'whileLoop']:
                        tokens.append(('KEYWORD', identifier))
                    elif identifier in ['open','high','low','close','volume','barIndex','barStateIsConfirmed','barStateIsFirst','barStateIsHistory','barStateIsLast','barStateIsLastConfirmedHistory','barStateIsNew','barStateIsRealtime','boxAll','chartBgCol','chartFgCol','chartIsHeikinAshi','chartIsKagi','chartIsLineBreak','chartIsPnf','chartIsRange','chartIsRenko','chartIsStandard','chartLeftVisibleBarTime','chartRightVisibleBarTime','dayOfMonth','dayOfWeek','dividendsFutureAmount','dividendsFutureExDate','dividendsFuturePayDate','earningsFutureEps','earningsFuturePeriodEndTime','earningsFutureRevenue','earningsFutureTime','hl2','hlc3','hlcc4','hour','labelAll','lastBarIndex','lastBarTime','lineAll','lineFillAll','minute','month','na','ohlc4','polylineAll','second','sessionIsFirstBar','sessionIsFirstBarRegular','sessionIsLastBar','sessionIsLastBarRegular','sessionIsMarket','sessionIsPostMarket','sessionIsPreMarket','strategyAccountCurrency','strategyAvgLosingTrade','strategyAvgLosingTradePercent','strategyAvgTrade','strategyAvgTradePercent','strategyAvgWinningTrade','strategyAvgWinningTradePercent','strategyClosedTrades','strategyClosedTradesFirstIndex','strategyEquity','strategyEvenTrades','strategyGrossLoss','strategyGrossLossPercent','strategyGrossProfit','strategyGrossProfitPercent','strategyInitialCapital','strategyLossTrades','strategyMarginLiquidationPrice','strategyMaxContractsHeldAll','strategyMaxContractsHeldLong','strategyMaxContractsHeldShort','strategyMaxDrawdown','strategyMaxDrawdownPercent','strategyMaxRunup','strategyMaxRunupPercent','strategyNetProfit','strategyNetProfitPercent','strategyOpenProfit','strategyOpenProfitPercent','strategyOpenTrades','strategyOpenTradesCapitalHeld','strategyPositionAvgPrice','strategyPositionEntryName','strategyPositionSize','strategyWinTrades','symInfoBaseCurrency','symInfoCountry','symInfoCurrency','symInfoDescription','symInfoEmployees','symInfoExpirationDate','symInfoIndustry','symInfoMainTickerId','symInfoMinContract','symInfoMinMove','symInfoMinTick','symInfoPointValue','symInfoPrefix','symInfoPriceScale','symInfoRecommendationsBuy','symInfoRecommendationsBuyStrong','symInfoRecommendationsDate','symInfoRecommendationsHold','symInfoRecommendationsSell','symInfoRecommendationsSellStrong','symInfoRecommendationsTotal','symInfoRoot','symInfoSector','symInfoSession','symInfoShareholders','symInfoSharesOutstandingFloat','symInfoSharesOutstandingTotal','symInfoTargetPriceAverage','symInfoTargetPriceDate','symInfoTargetPriceEstimates','symInfoTargetPriceHigh','symInfoTargetPriceLow','symInfoTargetPriceMedian','symInfoTicker','symInfoTickerId','symInfoTimezone','symInfoType','symInfoVolumeType','taAccDist','taIII','taNVI','taOBV','taPVI','taPVT','taTR','taVWAP','taWAD','taWVAD','tableAll','time','timeClose','timeTradingDay','timeframeIsDaily','timeframeIsDWM','timeframeIsIntraday','timeframeIsMinutes','timeframeIsMonthly','timeframeIsSeconds','timeframeIsTicks','timeframeIsWeekly','timeframeMainPeriod','timeframeMultiplier','timeframePeriod','timeNow','weekOfYear','year']:
                        tokens.append(('BUILTIN_VARIABLE', identifier))
                    elif identifier in ['sma', 'ema', 'rsi', 'minvalue', 'maxvalue','alertFunc', 'alertConditionFunc', 'arrAbs', 'arrAvg', 'arrBinarySearch', 'arrBinarySearchLeftmost', 'arrBinarySearchRightmost', 'arrClear', 'arrConcat', 'arrCopy', 'arrCovariance', 'arrEvery', 'arrFill', 'arrFirst', 'arrFrom', 'arrGet', 'arrIncludes', 'arrIndexOf', 'arrInsert', 'arrJoin', 'arrLast', 'arrLastIndexOf', 'arrMax', 'arrMedian', 'arrMin', 'arrMode', 'arrNewBool', 'arrNewBox', 'aryNewCol', 'arrNewFloat', 'arrNewInt', 'arrNewLabel', 'arrNewLine', 'arrNewLineFill', 'arrNewString', 'arrNewTable', 'arrNewType', 'arrPercentileLinearInterpolation', 'arrPercentileNearestRank', 'arrPercentRank', 'arrPop', 'arrPush', 'arrRange', 'arrRemove', 'arrReverse', 'arrSet', 'arrShift', 'arrSize', 'arrSlice', 'arrSome', 'arrSort', 'arrSortIndices', 'arrStandardize', 'arrStdev', 'arrSum', 'arrUnshift', 'arrVariance', 'barColFunc', 'bgColFunc', 'boolFunc', 'boxFunc', 'boxCopyFunc', 'boxDeleteFunc', 'boxGetBottomFunc', 'boxGetLeftFunc', 'boxGetRightFunc', 'boxGetTopFunc', 'boxNewFunc', 'boxSetBgColFunc', 'boxSetBorderColFunc', 'boxSetBorderStyleFunc', 'boxSetBorderWidthFunc', 'boxSetBottomFunc', 'boxSetBottomRightPointFunc', 'boxSetExtendFunc', 'boxSetLeftFunc', 'boxSetLeftTopFunc', 'boxSetRightFunc', 'boxSetRightBottomFunc', 'boxSetTextFunc', 'boxSetTextColFunc', 'boxSetTextFontFamilyFunc', 'boxSetTextHAlignFunc', 'boxSetTextSizeFunc', 'boxSetTextVAlignFunc', 'boxSetTextWrapFunc', 'boxSetTopFunc', 'boxSetTopLeftPointFunc', 'chartPointCopyFunc', 'chartPointFromIndexFunc', 'chartPointFromTimeFunc', 'chartPointNewFunc', 'chartPointNowFunc', 'colFunc', 'colBFunc', 'colFromGradientFunc', 'colGFunc', 'colNewFunc', 'colRFunc', 'colRgbFunc', 'colTFunc', 'dayOfMonthFunc', 'dayOfWeekFunc', 'fillFunc', 'fixNanFunc', 'floatFunc', 'hLineFunc', 'hourFunc', 'indicatorFunc', 'inputFunc', 'inputBoolFunc', 'inputColFunc', 'inputEnumFunc', 'inputFloatFunc', 'inputIntFunc', 'inputPriceFunc', 'inputSessionFunc', 'inputSourceFunc', 'inputStringFunc', 'inputSymbolFunc', 'inputTextAreaFunc', 'inputTimeFunc', 'inputTimeFrameFunc', 'intFunc', 'labelFunc', 'labelCopyFunc', 'labelDeleteFunc', 'labelGetTextFunc', 'labelGetXFunc', 'labelGetYFunc', 'labelNewFunc', 'labelSetColFunc', 'labelSetPointFunc', 'labelSetSizeFunc', 'labelSetStyleFunc', 'labelSetTextFunc', 'labelSetTextFontFamilyFunc', 'labelSetTextAlignFunc', 'labelSetTextColFunc', 'labelSetToolTipFunc', 'labelSetXFunc', 'labelSetXLocFunc', 'labelSetXYFunc', 'labelSetYFunc', 'labelSetYLocFunc', 'libraryFunc', 'lineFunc', 'lineCopyFunc', 'lineDeleteFunc', 'lineGetPriceFunc', 'lineGetX1Func', 'lineGetX2Func', 'lineGetY1Func', 'lineGetY2Func', 'lineNewFunc', 'lineSetColFunc', 'lineSetExtendFunc', 'lineSetFirstPointFunc', 'lineSetSecondPointFunc', 'lineSetStyleFunc', 'lineSetWidthFunc', 'lineSetX1Func', 'lineSetX2Func', 'lineSetXLocFunc', 'lineSetXY1Func', 'lineSetXY2Func', 'lineSetY1Func', 'lineSetY2Func', 'lineFillFunc', 'lineFillDeleteFunc', 'lineFillGetLine1Func', 'lineFillGetLine2Func', 'lineFillNewFunc', 'lineFillSetColFunc', 'logErrorFunc', 'logInfoFunc', 'logWarningFunc', 'mapClearFunc', 'mapContainsFunc', 'mapCopyFunc', 'mapGetFunc', 'mapKeysFunc', 'mapNewTypeFunc', 'mapPutFunc', 'mapPutAllFunc', 'mapRemoveFunc', 'mapSizeFunc', 'mapValuesFunc', 'mathAbsFunc', 'mathAcosFunc', 'mathAsinFunc', 'mathAtanFunc', 'mathAvgFunc', 'mathCeilFunc', 'mathCosFunc', 'mathExpFunc', 'mathFloorFunc', 'mathLogFunc', 'mathLog10Func', 'mathMaxFunc', 'mathMinFunc', 'mathPowFunc', 'mathRandomFunc', 'mathRoundFunc', 'mathRoundToMinTickFunc', 'mathSignFunc', 'mathSinFunc', 'mathSqrtFunc', 'mathSumFunc', 'mathTanFunc', 'mathToDegreesFunc', 'mathToRadiansFunc', 'matrixAddColFunc', 'matrixAddRowFunc', 'matrixAvgFunc', 'matrixColFunc', 'matrixColumnsFunc', 'matrixConcatFunc', 'matrixCopyFunc', 'matrixDetFunc', 'matrixDiffFunc', 'matrixEigenValuesFunc', 'matrixEigenVectorsFunc', 'matrixElementsCountFunc', 'matrixFillFunc', 'matrixGetFunc', 'matrixInvFunc', 'matrixIsAntiDiagonalFunc', 'matrixIsAntiSymmetricFunc', 'matrixIsBinaryFunc', 'matrixIsDiagonalFunc', 'matrixIsIdentityFunc', 'matrixIsSquareFunc', 'matrixIsStochasticFunc', 'matrixIsSymmetricFunc', 'matrixIsTriangularFunc', 'matrixIsZeroFunc', 'matrixKronFunc', 'matrixMaxFunc', 'matrixMedianFunc', 'matrixMinFunc', 'matrixModeFunc', 'matrixMultFunc', 'matrixNewTypeFunc', 'matrixPinvFunc', 'matrixPowFunc', 'matrixRankFunc', 'matrixRemoveColFunc', 'matrixRemoveRowFunc', 'matrixReshapeFunc', 'matrixReverseFunc', 'matrixRowFunc', 'matrixRowsFunc', 'matrixSetFunc', 'matrixSortFunc', 'matrixSubMatrixFunc', 'matrixSumFunc', 'matrixSwapColumnsFunc', 'matrixSwapRowsFunc', 'matrixTraceFunc', 'matrixTransposeFunc', 'maxBarsBackFunc', 'minuteFunc', 'monthFunc', 'naFunc', 'nzFunc', 'polylineDeleteFunc', 'polylineNewFunc', 'requestCurrencyRateFunc', 'requestDividendsFunc', 'requestEarningsFunc', 'requestEconomicFunc', 'requestFinancialFunc', 'requestQuandlFunc', 'requestSecurityFunc', 'requestSecurityLowerTfFunc', 'requestSeedFunc', 'requestSplitsFunc', 'runtimeErrorFunc', 'secondFunc', 'strContainsFunc', 'strEndsWithFunc', 'strFormatFunc', 'strFormatTimeFunc', 'strLengthFunc', 'strLowerFunc', 'strMatchFunc', 'strPosFunc', 'strRepeatFunc', 'strReplaceFunc', 'strReplaceAllFunc', 'strSplitFunc', 'strStartsWithFunc', 'strSubstringFunc', 'strToNumberFunc', 'strToStringFunc', 'strTrimFunc', 'strUpperFunc', 'strategyFunc', 'strategyCancelFunc', 'strategyCancelAllFunc', 'strategyCloseFunc', 'strategyCloseAllFunc', 'strategyClosedTradesCommissionFunc', 'strategyClosedTradesEntryBarIndexFunc', 'strategyClosedTradesEntryCommentFunc', 'strategyClosedTradesEntryIdFunc', 'strategyClosedTradesEntryPriceFunc', 'strategyClosedTradesEntryTimeFunc', 'strategyClosedTradesExitBarIndexFunc', 'strategyClosedTradesExitCommentFunc', 'strategyClosedTradesExitIdFunc', 'strategyClosedTradesExitPriceFunc', 'strategyClosedTradesExitTimeFunc', 'strategyClosedTradesMaxDrawdownFunc', 'strategyClosedTradesMaxDrawdownPercentFunc', 'strategyClosedTradesMaxRunupFunc', 'strategyClosedTradesMaxRunupPercentFunc', 'strategyClosedTradesProfitFunc', 'strategyClosedTradesProfitPercentFunc', 'strategyClosedTradesSizeFunc', 'strategyConvertToAccountFunc', 'strategyConvertToSymbolFunc', 'strategyDefaultEntryQtyFunc', 'strategyEntryFunc', 'strategyExitFunc', 'strategyOpenTradesCommissionFunc', 'strategyOpenTradesEntryBarIndexFunc', 'strategyOpenTradesEntryCommentFunc', 'strategyOpenTradesEntryIdFunc', 'strategyOpenTradesEntryPriceFunc', 'strategyOpenTradesEntryTimeFunc', 'strategyOpenTradesMaxDrawdownFunc', 'strategyOpenTradesMaxDrawdownPercentFunc', 'strategyOpenTradesMaxRunupFunc', 'strategyOpenTradesMaxRunupPercentFunc', 'strategyOpenTradesProfitFunc', 'strategyOpenTradesProfitPercentFunc', 'strategyOpenTradesSizeFunc', 'strategyOrderFunc', 'strategyRiskAllowEntryInFunc', 'strategyRiskMaxConsLossDaysFunc', 'strategyRiskMaxDrawdownFunc', 'strategyRiskMaxIntradayFilledOrdersFunc', 'strategyRiskMaxIntradayLossFunc', 'strategyRiskMaxPositionSizeFunc', 'symInfoPrefixFunc', 'symInfoTickerFunc', 'timeFunc', 'timeCloseFunc', 'timeframeChangeFunc', 'timeframeFromSecondsFunc', 'timeframeInSecondsFunc', 'timestampFunc', 'weekOfYearFunc', 'yearFunc']:
                        tokens.append(('BUILTIN_FUNCTION', identifier))
                    elif identifier == 'true' or identifier == 'false':
                        tokens.append(('BOOLEAN', identifier == 'true'))
                    elif identifier in ['showStyleArea','showStyleAreaBr','showStyleCircles','showStyleColumns','showStyleCross','showStyleHistogram','showStyleLine','showStyleLineBr','showStyleStepLine','showStyleStepLineDiamond','showStyleStepLineBr','positionBottomCenter','positionBottomLeft','positionBottomRight','positionMiddleCenter','positionMiddleLeft','positionMiddleRight','positionTopCenter','positionTopLeft','positionTopRight','scaleLeft','scaleNone','scaleRight','sessionExtended','sessionRegular','settlementAsCloseInherit','settlementAsCloseOff','settlementAsCloseOn','shapeArrowDown','shapeArrowUp','shapeCircle','shapeCross','shapeDiamond','shapeFlag','shapeLabelDown','shapeLabelUp','shapeSquare','shapeTriangleDown','shapeTriangleUp','shapeXCross','sizeAuto','sizeHuge','sizeLarge','sizeNormal','sizeSmall','sizeTiny','splitsDenominator','splitsNumerator','strategyCash','strategyCommissionCashPerContract','strategyCommissionCashPerOrder','strategyCommissionPercent','strategyDirectionAll','strategyDirectionLong','strategyDirectionShort','strategyFixed','strategyLong','strategyOcaCancel','strategyOcaNone','strategyOcaReduce','strategyPercentOfEquity','strategyShort','textAlignBottom','textAlignCenter','textAlignLeft','textAlignRight','textAlignTop','textWrapAuto','textWrapNone','trueValue','xLocBarIndex','xLocBarTime','yLocAboveBar','yLocBelowBar','yLocPrice','adjustmentDividends','adjustmentNone','adjustmentSplits','alertFreqAll','alertFreqOncePerBar','alertFreqOncePerBarClose','backAdjustmentInherit','backAdjustmentOff','backAdjustmentOn','barMergeGapsOff','barMergeGapsOn','barMergeLookaheadOff','barMergeLookaheadOn','colAqua','colBlack','colBlue','colFuchsia','colGray','colGreen','colLime','colMaroon','colNavy','colOlive','colOrange','colPurple','colRed','colSilver','colTeal','colWhite','colYellow','currencyAUD','currencyBTC','currencyCAD','currencyCHF','currencyETH','currencyEUR','currencyGBP','currencyHKD','currencyINR','currencyJPY','currencyKRW','currencyMYR','currencyNOK','currencyNone','currencyNZD','currencyRUB','currencySEK','currencySGD','currencyTRY','currencyUSD','currencyUSDT','currencyZAR','dayOfWeekFriday','dayOfWeekMonday','dayOfWeekSaturday','dayOfWeekSunday','dayOfWeekThursday','dayOfWeekTuesday','dayOfWeekWednesday','displayAll','displayDataWindow','displayNone','displayPane','displayPriceScale','displayStatusLine','dividendsGross','dividendsNet','earningsActual','earningsEstimate','earningsStandardized','extendBoth','extendLeft','extendNone','extendRight','falseValue','fontFamilyDefault','fontFamilyMonospace','formatInherit','formatMinTick','formatPercent','formatPrice','formatVolume','hlineStyleDashed','hlineStyleDotted','hlineStyleSolid','labelStyleArrowDown','labelStyleArrowUp','labelStyleCircle','labelStyleCross','labelStyleDiamond','labelStyleFlag','labelStyleLabelCenter','labelStyleLabelDown','labelStyleLabelLeft','labelStyleLabelLowerLeft','labelStyleLabelLowerRight','labelStyleLabelRight','labelStyleLabelUp','labelStyleLabelUpperLeft','labelStyleLabelUpperRight','labelStyleNone','labelStyleSquare','labelStyleTextOutline','labelStyleTriangleDown','labelStyleTriangleUp','labelStyleXCross','lineStyleArrowBoth','lineStyleArrowLeft','lineStyleArrowRight','lineStyleDashed','lineStyleDotted','lineStyleSolid','locationAboveBar','locationAbsolute','locationBelowBar','locationBottom','locationTop','mathE','mathPhi','mathPi','mathRPhi','orderAscending','orderDescending']:
                        tokens.append(('CONSTANT', identifier))
                    elif identifier in ['arr', 'bool', 'box', 'chartPoint', 'col', 'const', 'float', 'int', 'label', 'line', 'lineFill', 'map', 'matrx', 'polyline', 'series', 'simple', 'string', 'table']:
                        tokens.append(('TYPE_DECLARATION', identifier))
                    else:
                        tokens.append(('IDENTIFIER', identifier))
                    self.current_position += match.end()
                    continue
            
            elif char in ['+', '-', '*', '/', '%', '=', '>', '<', '!', '=']:
                if char == '=' and self.peek() == '=':
                    tokens.append(('OPERATOR', '=='))
                    self.current_position += 2
                elif char == '!' and self.peek() == '=':
                    tokens.append(('OPERATOR', '!='))
                    self.current_position += 2
                elif char == '>' and self.peek() == '=':
                    tokens.append(('OPERATOR', '>='))
                    self.current_position += 2
                elif char == '<' and self.peek() == '=':
                    tokens.append(('OPERATOR', '<='))
                    self.current_position += 2
                else:
                    tokens.append(('OPERATOR', char))
                    self.current_position += 1
                continue
            
            elif char == '(':
                tokens.append(('LPAREN', char))
                self.current_position += 1
                continue
            elif char == ')':
                tokens.append(('RPAREN', char))
                self.current_position += 1
                continue
            elif char == '{':
                tokens.append(('LBRACE', char))
                self.current_position += 1
                continue
            elif char == '}':
                tokens.append(('RBRACE', char))
                self.current_position += 1
                continue
            elif char == ',':
                tokens.append(('COMMA', char))
                self.current_position += 1
                continue
            elif char == ':':
                tokens.append(('COLON', char))
                self.current_position += 1
                continue
            elif char == '"':
                self.current_position += 1
                start = self.current_position
                while self.current_position < len(self.source_code) and self.source_code[self.current_position] != '"':
                    self.current_position += 1
                tokens.append(('STRING', self.source_code[start:self.current_position]))
                self.current_position += 1
                continue

            self.current_position += 1 # Skip characters we don't recognize for now
        return tokens

    def peek(self):
        if self.current_position + 1 < len(self.source_code):
            return self.source_code[self.current_position + 1]
        return None
    



"""-----------------------------------------------------------------------------------------------------------------------------------------"""

# Parser



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    
    def parse(self):
        # Market Data & Price Variables
        if self._match(['open', 'high', 'low', 'close', 'volume', 'hl2', 'hlc3', 'hlcc4', 'ohlc4',
                       'symInfoMinMove', 'symInfoMinTick', 'symInfoPointValue', 'symInfoPrefix',
                       'symInfoPriceScale', 'symInfoRoot', 'symInfoSector', 'symInfoSession',
                       'symInfoShareholders', 'symInfoSharesOutstandingFloat',
                       'symInfoSharesOutstandingTotal']):
            return self.parse_market_data()
    
        # Technical Analysis & Indicators
        elif self._match(['taAccDist', 'taIII', 'taNVI', 'taOBV', 'taPVI', 'taPVT', 'taTR', 'taVWAP',
                         'taWAD', 'taWVAD', 'taAlma', 'taAtr', 'taBarsSince', 'taBb', 'taBbw', 'taCci',
                         'taChange', 'taCmo', 'taCog', 'taCorrelation', 'taCross', 'taCrossover',
                         'taCrossunder', 'taCum', 'taDev', 'taDmi', 'taEma', 'taFalling', 'taHighest',
                         'taHighestBars', 'taHma', 'taKc', 'taKcw', 'taLinReg', 'taLowest',
                         'taLowestBars', 'taMacd', 'taMax', 'taMedian', 'taMfi', 'taMin', 'taMode',
                         'taMom', 'taPercentile', 'taPercentRank', 'taPivotHigh', 'taPivotLow',
                         'taRange', 'taRising', 'taRma', 'taRoc', 'taRsi', 'taSar', 'taSma', 'taStdev',
                         'taStoch', 'taSuperTrend', 'taSwma', 'taTsi', 'taValueWhen', 'taVariance',
                         'taVwap', 'taVwma', 'taWma', 'taWpr']):
            return self.parse_technical_analysis()
    
        # Strategy & Trading Functions
        elif self._match(['strategyAccountCurrency', 'strategyAvgLosingTrade',
                         'strategyAvgLosingTradePercent', 'strategyAvgTrade',
                         'strategyAvgTradePercent', 'strategyAvgWinningTrade',
                         'strategyAvgWinningTradePercent', 'strategyClosedTrades',
                         'strategyClosedTradesFirstIndex', 'strategyEquity', 'strategyEvenTrades',
                         'strategyGrossLoss', 'strategyGrossLossPercent', 'strategyGrossProfit',
                         'strategyGrossProfitPercent', 'strategyInitialCapital', 'strategyLossTrades',
                         'strategyMarginLiquidationPrice', 'strategyMaxContractsHeldAll',
                         'strategyMaxContractsHeldLong', 'strategyMaxContractsHeldShort',
                         'strategyMaxDrawdown', 'strategyMaxDrawdownPercent', 'strategyMaxRunup',
                         'strategyMaxRunupPercent', 'strategyNetProfit', 'strategyNetProfitPercent',
                         'strategyOpenProfit', 'strategyOpenProfitPercent', 'strategyOpenTrades',
                         'strategyOpenTradesCapitalHeld', 'strategyPositionAvgPrice',
                         'strategyPositionEntryName', 'strategyPositionSize', 'strategyWinTrades']):
            return self.parse_strategy()
    
        # Chart & Visual Elements
        elif self._match(['boxAll', 'chartBgCol', 'chartFgCol', 'chartIsHeikinAshi',
                         'chartIsKagi', 'chartIsLineBreak', 'chartIsPnf', 'chartIsRange',
                         'chartIsRenko', 'chartIsStandard', 'chartLeftVisibleBarTime',
                         'chartRightVisibleBarTime', 'labelAll', 'lineAll', 'lineFillAll',
                         'polylineAll', 'tableAll']):
            return self.parse_chart_elements()
    
        # Time & Session Functions
        elif self._match(['dayOfMonth', 'dayOfWeek', 'hour', 'minute', 'month',
                         'second', 'time', 'timeClose', 'timeTradingDay', 'timeNow',
                         'weekOfYear', 'year', 'sessionIsFirstBar', 'sessionIsFirstBarRegular',
                         'sessionIsLastBar', 'sessionIsLastBarRegular', 'sessionIsMarket',
                         'sessionIsPostMarket', 'sessionIsPreMarket']):
            return self.parse_time_session()
    
        # Symbol Information
        elif self._match(['symInfoRecommendationsBuy', 'symInfoRecommendationsBuyStrong',
                         'symInfoRecommendationsDate', 'symInfoRecommendationsHold',
                         'symInfoRecommendationsSell', 'symInfoRecommendationsSellStrong',
                         'symInfoRecommendationsTotal', 'symInfoTargetPriceAverage',
                         'symInfoTargetPriceDate', 'symInfoTargetPriceEstimates',
                         'symInfoTargetPriceHigh', 'symInfoTargetPriceLow',
                         'symInfoTargetPriceMedian', 'symInfoTicker', 'symInfoTickerId',
                         'symInfoTimezone', 'symInfoType', 'symInfoVolumeType']):
            return self.parse_symbol_info()
    
        # Constants & Style Elements
        elif self._match(['adjustmentDividends', 'adjustmentNone', 'adjustmentSplits',
                         'alertFreqAll', 'alertFreqOncePerBar', 'alertFreqOncePerBarClose',
                         'colAqua', 'colBlack', 'colBlue', 'colFuchsia', 'colGray',
                         'colGreen', 'colLime', 'colMaroon', 'colNavy', 'colOlive',
                         'colOrange', 'colPurple', 'colRed', 'colSilver', 'colTeal',
                         'colWhite', 'colYellow']):
            return self.parse_constants_and_styles()
    
        # Matrix Operations
        elif self._match(['matrixAddCol', 'matrixAddRow', 'matrixAvg', 'matrixCol',
                         'matrixColumns', 'matrixConcat', 'matrixCopy', 'matrixDet',
                         'matrixDiff', 'matrixEigenValues', 'matrixEigenVectors',
                         'matrixElementsCount', 'matrixFill', 'matrixGet', 'matrixInv']):
            return self.parse_matrix_operations()
    
        
        # Market Data Variables
        elif self._match(['open', 'high', 'low', 'close', 'volume', 'hl2', 'hlc3', 'hlcc4', 'ohlc4']):
            return self.parse_market_data()
            
        # Bar State Variables
        elif self._match(['barIndex', 'barStateIsConfirmed', 'barStateIsFirst', 'barStateIsHistory',
                         'barStateIsLast', 'barStateIsLastConfirmedHistory', 'barStateIsNew',
                         'barStateIsRealtime', 'lastBarIndex', 'lastBarTime']):
            return self.parse_bar_state()
            
        # Chart Variables
        elif self._match(['boxAll', 'chartBgCol', 'chartFgCol', 'chartIsHeikinAshi', 'chartIsKagi',
                         'chartIsLineBreak', 'chartIsPnf', 'chartIsRange', 'chartIsRenko',
                         'chartIsStandard', 'chartLeftVisibleBarTime', 'chartRightVisibleBarTime']):
            return self.parse_chart_variable()
            
        # Time Variables
        elif self._match(['dayOfMonth', 'dayOfWeek', 'hour', 'minute', 'month', 'second',
                         'time', 'timeClose', 'timeTradingDay', 'timeNow', 'weekOfYear', 'year']):
            return self.parse_time_variable()
            
        # Session Variables
        elif self._match(['sessionIsFirstBar', 'sessionIsFirstBarRegular', 'sessionIsLastBar',
                         'sessionIsLastBarRegular', 'sessionIsMarket', 'sessionIsPostMarket',
                         'sessionIsPreMarket']):
            return self.parse_session_variable()
            
        # Timeframe Variables
        elif self._match(['timeframeIsDaily', 'timeframeIsDWM', 'timeframeIsIntraday',
                         'timeframeIsMinutes', 'timeframeIsMonthly', 'timeframeIsSeconds',
                         'timeframeIsTicks', 'timeframeIsWeekly', 'timeframeMainPeriod',
                         'timeframeMultiplier', 'timeframePeriod']):
            return self.parse_timeframe_variable()
            
        # Symbol Info Variables
        elif self._match(['symInfoBaseCurrency', 'symInfoCountry', 'symInfoCurrency',
                         'symInfoDescription', 'symInfoEmployees', 'symInfoExpirationDate',
                         'symInfoIndustry', 'symInfoMainTickerId', 'symInfoMinContract']):
            return self.parse_symbol_info()
            
        # Technical Analysis Variables
        elif self._match(['taAccDist', 'taIII', 'taNVI', 'taOBV', 'taPVI', 'taPVT',
                         'taTR', 'taVWAP', 'taWAD', 'taWVAD']):
            return self.parse_technical_analysis()
            
        # Strategy Variables
        elif self._match(['strategyAccountCurrency', 'strategyAvgLosingTrade',
                         'strategyAvgWinningTrade', 'strategyClosedTrades',
                         'strategyEquity', 'strategyNetProfit']):
            return self.parse_strategy_variable()
            
        # Drawing Objects
        elif self._match(['labelAll', 'lineAll', 'lineFillAll', 'polylineAll', 'tableAll']):
            return self.parse_drawing_object()
            
        # Financial Data Variables
        elif self._match(['dividendsFutureAmount', 'dividendsFutureExDate',
                         'earningsFutureEps', 'earningsFutureRevenue']):
            return self.parse_financial_data()
            
        # Constants and Special Values
        elif self._match(['na', 'mathE', 'mathPi', 'mathPhi', 'trueValue', 'falseValue']):
            return self.parse_constant()
            
        # Style Constants
        elif self._match(['colAqua', 'colBlack', 'colBlue', 'colFuchsia', 'colGray',
                         'lineStyleArrowBoth', 'lineStyleDashed', 'lineStyleDotted',
                         'showStyleArea', 'showStyleCircles', 'showStyleColumns']):
            return self.parse_style_constant()
            
        
        # Data Types
        elif self._match(['Numeric', 'Boolean', 'String', 'Series']):
            return self.parse_data_type()
            
        # Variable Declaration
        elif self._match('let'):
            return self.parse_variable_declaration()
            
        # Operators
        elif self._match(['=', '+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=', 'and', 'or', 'not']):
            return self.parse_operator()
            
        # Built-in Variables
        elif self._match(['open', 'high', 'low', 'close', 'volume', 'barIndex', 
                         'barStateIsConfirmed', 'barStateIsFirst', 'barStateIsHistory',
                         'barStateIsLast', 'barStateIsLastConfirmedHistory', 'barStateIsNew',
                         'barStateIsRealtime', 'boxAll', 'chartBgCol', 'chartFgCol']):
            return self.parse_builtin_variable()
            
        # Control Flow
        elif self._match(['if', 'else', 'for', 'while']):
            return self.parse_control_flow()
            
        # Arrays
        elif self._match(['[', ']']):
            return self.parse_array()
            
        # Functions
        elif self._match('define'):
            return self.parse_function_definition()
            
        # Built-in Functions
        elif self._match(['sma', 'ema', 'rsi']):
            return self.parse_builtin_function()
            
        # Comments
        elif self._match('//'): 
            return self.parse_comment()
            
        # Input Declarations
        elif self._match('param'):
            return self.parse_input_declaration()
            
        # Colors
        elif self._match(['red', 'blue', 'green', 'yellow', 'black', 'white']):
            return self.parse_color()
            
        # Plotting
        elif self._match(['show', 'showshape', 'showcond']):
            return self.parse_plotting()
            
        # Drawing Tools
        elif self._match(['drawline', 'drawrect']):
            return self.parse_drawing()
            
        # Alerts
        elif self._match('alert'):
            return self.parse_alert()
            
        # Events
        elif self._match(['onTick', 'onBar']):
            return self.parse_event()
            
        # Error Handling
        elif self._match(['try', 'catch']):
            return self.parse_error_handling()
            
        # Line Style
        elif self._match(['solid', 'dotted', 'dashed']):
            return self.parse_line_style()
            
        # Shape Style
        elif self._match(['size', 'color']):
            return self.parse_shape_style()
            
        # Constants
        elif self._match(['adjustmentDividends', 'adjustmentNone', 'adjustmentSplits',
                         'alertFreqAll', 'alertFreqOncePerBar', 'alertFreqOncePerBarClose']):
            return self.parse_constant()
            
        # Type Declarations
        elif self._match(['arr', 'bool', 'box', 'chartPoint', 'col', 'const', 'float',
                         'int', 'label', 'line', 'lineFill', 'map', 'matrx', 'polyline',
                         'series', 'simple', 'string', 'table']):
            return self.parse_type_declaration()
            
        # Keywords
        elif self._match(['andOp', 'enumType', 'exportFunc', 'forLoop', 'forInLoop',
                         'ifCond', 'importFunc', 'methodFunc', 'notOp', 'orOp',
                         'switchCase', 'typeDef', 'whileLoop']):
            return self.parse_keyword()
    
        # Currency Constants
        elif self._match(['currencyAUD', 'currencyBTC', 'currencyCAD', 'currencyCHF', 'currencyETH', 
                       'currencyEUR', 'currencyGBP', 'currencyHKD', 'currencyINR', 'currencyJPY', 
                       'currencyKRW', 'currencyMYR', 'currencyNOK', 'currencyNone', 'currencyNZD', 
                       'currencyRUB', 'currencySEK', 'currencySGD', 'currencyTRY', 'currencyUSD', 
                       'currencyUSDT', 'currencyZAR']):
            return self.parse_currency()
    
        # Display Constants
        elif self._match(['displayAll', 'displayDataWindow', 'displayNone', 'displayPane', 
                         'displayPriceScale', 'displayStatusLine']):
            return self.parse_display()
    
        # Dividends & Earnings
        elif self._match(['dividendsGross', 'dividendsNet', 'earningsActual', 
                         'earningsEstimate', 'earningsStandardized']):
            return self.parse_financial_metrics()
    
        # Extension Types
        elif self._match(['extendBoth', 'extendLeft', 'extendNone', 'extendRight']):
            return self.parse_extension()
    
        # Font Styles
        elif self._match(['fontFamilyDefault', 'fontFamilyMonospace']):
            return self.parse_font()
    
        # Format Types
        elif self._match(['formatInherit', 'formatMinTick', 'formatPercent', 
                         'formatPrice', 'formatVolume']):
            return self.parse_format()
    
        # Line Styles
        elif self._match(['hlineStyleDashed', 'hlineStyleDotted', 'hlineStyleSolid']):
            return self.parse_line_style()
    
        # Label Styles
        elif self._match(['labelStyleArrowDown', 'labelStyleArrowUp', 'labelStyleCircle', 
                         'labelStyleCross', 'labelStyleDiamond', 'labelStyleFlag', 
                         'labelStyleLabelCenter', 'labelStyleLabelDown', 'labelStyleLabelLeft', 
                         'labelStyleLabelLowerLeft', 'labelStyleLabelLowerRight', 
                         'labelStyleLabelRight', 'labelStyleLabelUp', 'labelStyleLabelUpperLeft', 
                         'labelStyleLabelUpperRight', 'labelStyleNone', 'labelStyleSquare', 
                         'labelStyleTextOutline', 'labelStyleTriangleDown', 'labelStyleTriangleUp', 
                         'labelStyleXCross']):
            return self.parse_label_style()
    
        # Position Constants
        elif self._match(['positionBottomCenter', 'positionBottomLeft', 'positionBottomRight', 
                         'positionMiddleCenter', 'positionMiddleLeft', 'positionMiddleRight', 
                         'positionTopCenter', 'positionTopLeft', 'positionTopRight']):
            return self.parse_position()
    
        # Scale Types
        elif self._match(['scaleLeft', 'scaleNone', 'scaleRight']):
            return self.parse_scale()
    
        # Shape Types
        elif self._match(['shapeArrowDown', 'shapeArrowUp', 'shapeCircle', 'shapeCross', 
                         'shapeDiamond', 'shapeFlag', 'shapeLabelDown', 'shapeLabelUp', 
                         'shapeSquare', 'shapeTriangleDown', 'shapeTriangleUp', 'shapeXCross']):
            return self.parse_shape()
    
        # Size Constants
        elif self._match(['sizeAuto', 'sizeHuge', 'sizeLarge', 'sizeNormal', 
                         'sizeSmall', 'sizeTiny']):
            return self.parse_size()
    
        # Text Alignment
        elif self._match(['textAlignBottom', 'textAlignCenter', 'textAlignLeft', 
                         'textAlignRight', 'textAlignTop', 'textWrapAuto', 'textWrapNone']):
            return self.parse_text_alignment()
    
        # Location Types
        elif self._match(['xLocBarIndex', 'xLocBarTime', 'yLocAboveBar', 
                         'yLocBelowBar', 'yLocPrice']):
            return self.parse_location()
    
    
        return self.parse_default_identifier()
    

    def parse_variable_declaration(self):
        self.current_token_index += 1  # Consume 'let'
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'IDENTIFIER':
            variable_name = self.tokens[self.current_token_index][1]
            self.current_token_index += 1  # Consume identifier
            if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'OPERATOR' and self.tokens[self.current_token_index][1] == '=':
                self.current_token_index += 1  # Consume '='
                right_hand_side = self.parse_expression()
                if right_hand_side:
                    return {'type': 'variable_declaration', 'name': variable_name, 'value': right_hand_side}

    def parse_if_statement(self):
        self._consume()  # Consume 'if'
        if not self._match('LPAREN'):
            raise Exception("Expected '(' after 'if'")
        self._consume()  # Consume '('
        
        condition = self.parse_expression()
        
        if not self._match('RPAREN'):
            raise Exception("Expected ')' after if condition")
        self._consume()  # Consume ')'
        
        body = self.parse()
        
        return {'type': 'if_statement', 'condition': condition, 'body': body}

    def parse_function_declaration(self):
        self.current_token_index += 1  # Consume 'define'
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'IDENTIFIER':
            function_name = self.tokens[self.current_token_index][1]
            self.current_token_index += 1  # Consume identifier
            if self._match('LPAREN'):
                self._consume()  # Consume '('
                parameters = []
                while not self._match('RPAREN'):
                    if self._match('IDENTIFIER'):
                        parameters.append(self._consume().value)
                    if self._match('COMMA'):
                        self._consume()  # Consume ','
                self._consume()  # Consume ')'
                body = self.parse_block()
                return {'type': 'function_declaration', 'name': function_name, 'parameters': parameters, 'body': body}

    def parse_function_call(self):
        function_name = self._consume().value
        self._consume()  # Consume '('
        arguments = []
        while not self._match('RPAREN'):
            arguments.append(self.parse_expression())
            if self._match('COMMA'):
                self._consume()  # Consume ','
        self._consume()  # Consume ')'
        return {'type': 'function_call', 'name': function_name, 'arguments': arguments}

    def parse_param_declaration(self):
        self.current_token_index += 1  # Consume 'param'
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'IDENTIFIER':
            param_name = self.tokens[self.current_token_index][1]
            self.current_token_index += 1  # Consume identifier
            if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'OPERATOR' and self.tokens[self.current_token_index][1] == '=':
                self.current_token_index += 1  # Consume '='
                default_value = self.parse_expression()
                if default_value:
                    return {'type': 'param_declaration', 'name': param_name, 'default_value': default_value}

    def parse_script_declaration(self):
        self.current_token_index += 1  # Consume 'script'
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == 'LPAREN':
            self._consume()  # Consume '('
            if self._match('STRING'):
                title = self._consume().value
                if self._match('RPAREN'):
                    self._consume()  # Consume ')'
                    return {'type': 'script_declaration', 'title': title}

    def parse_event(self, event_type):
        self.current_token_index += 1  # Consume event keyword
        body = self.parse_block()
        return {'type': 'event', 'event_type': event_type, 'body': body}

    def parse_try_catch(self):
        self._consume()  # Consume 'try'
        try_block = self.parse_block()
        if self._match('KEYWORD', 'catch'):
            self._consume()  # Consume 'catch'
            catch_block = self.parse_block()
            return {'type': 'try_catch', 'try_block': try_block, 'catch_block': catch_block}

    def parse_for_loop(self):
        self._consume()  # Consume 'for'
        if not self._match('IDENTIFIER'):
            raise Exception("Expected identifier after 'for'")
        loop_var = self._consume().value
        if not self._match('OPERATOR', '='):
            raise Exception("Expected '=' after loop variable")
        self._consume()  # Consume '='
        start_expr = self.parse_expression()
        if not self._match('KEYWORD', 'to'):
            raise Exception("Expected 'to' after start expression")
        self._consume()  # Consume 'to'
        end_expr = self.parse_expression()
        body = self.parse_block()
        return {'type': 'for_loop', 'loop_var': loop_var, 'start_expr': start_expr, 'end_expr': end_expr, 'body': body}

    def parse_while_loop(self):
        self._consume()  # Consume 'while'
        condition = self.parse_expression()
        body = self.parse_block()
        return {'type': 'while_loop', 'condition': condition, 'body': body}

    def parse_show(self):
        self._consume()  # Consume 'show'
        series = self.parse_expression()
        color = None
        linewidth = None
        if self._match('KEYWORD', 'col'):
            self._consume()  # Consume 'col'
            color = self.parse_expression()
        if self._match('KEYWORD', 'linewidth'):
            self._consume()  # Consume 'linewidth'
            linewidth = self.parse_expression()
        return {'type': 'show', 'series': series, 'color': color, 'linewidth': linewidth}

    def parse_showshape(self):
        self._consume()  # Consume 'showshape'
        shape = self.parse_expression()
        x_series = None
        y_series = None
        color = None
        size = None
        if self._match('KEYWORD', 'x'):
            self._consume()  # Consume 'x'
            x_series = self.parse_expression()
        if self._match('KEYWORD', 'y'):
            self._consume()  # Consume 'y'
            y_series = self.parse_expression()
        if self._match('KEYWORD', 'col'):
            self._consume()  # Consume 'col'
            color = self.parse_expression()
        if self._match('KEYWORD', 'size'):
            self._consume()  # Consume 'size'
            size = self.parse_expression()
        return {'type': 'showshape', 'shape': shape, 'x_series': x_series, 'y_series': y_series, 'color': color, 'size': size}

    def parse_showcond(self):
        self._consume()  # Consume 'showcond'
        condition = self.parse_expression()
        show_command = self.parse()
        return {'type': 'showcond', 'condition': condition, 'show_command': show_command}

    def parse_drawline(self):
        self._consume()  # Consume 'drawline'
        x1 = self.parse_expression()
        y1 = self.parse_expression()
        x2 = self.parse_expression()
        y2 = self.parse_expression()
        color = None
        width = None
        if self._match('KEYWORD', 'col'):
            self._consume()  # Consume 'col'
            color = self.parse_expression()
        if self._match('KEYWORD', 'width'):
            self._consume()  # Consume 'width'
            width = self.parse_expression()
        return {'type': 'drawline', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': color, 'width': width}

    def parse_drawrect(self):
        self._consume()  # Consume 'drawrect'
        x1 = self.parse_expression()
        y1 = self.parse_expression()
        x2 = self.parse_expression()
        y2 = self.parse_expression()
        color = None
        fill = None
        if self._match('KEYWORD', 'col'):
            self._consume()  # Consume 'col'
            color = self.parse_expression()
        if self._match('KEYWORD', 'fill'):
            self._consume()  # Consume 'fill'
            fill = self.parse_expression()
        return {'type': 'drawrect', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'color': color, 'fill': fill}

    def parse_alert(self):
        self._consume()  # Consume 'alert'
        condition = self.parse_expression()
        message = self.parse_expression()
        return {'type': 'alert', 'condition': condition, 'message': message}

    def parse_block(self):
        if not self._match('LBRACE'):
            return self.parse_expression()
        self._consume()  # Consume '{'
        statements = []
        while not self._match('RBRACE'):
            statements.append(self.parse())
        self._consume()  # Consume '}'
        return {'type': 'block', 'statements': statements}

    def parse_expression(self):
        if self._match('IDENTIFIER') and self.peek() == '(':
            return self.parse_function_call()
        elif self._match('BUILTIN_FUNCTION') and self.peek() == '(':
            return self.parse_function_call()
        return self.parse_addition()

    def parse_addition(self):
        left = self.parse_multiplication()
        while self._match('OPERATOR', '+') or self._match('OPERATOR', '-'):
            op = self._consume().value
            right = self.parse_multiplication()
            left = {'type': 'binary_op', 'op': op, 'left': left, 'right': right}
        return left

    def parse_multiplication(self):
        left = self.parse_primary()
        while self._match('OPERATOR', '*') or self._match('OPERATOR', '/'):
            op = self._consume().value
            right = self.parse_primary()
            left = {'type': 'binary_op', 'op': op, 'left': left, 'right': right}
        return left

    def parse_primary(self):
        if self._match('NUMBER'):
            return {'type': 'number', 'value': self._consume().value}
        elif self._match('BUILTIN_VARIABLE'):
            return {'type': 'builtin_variable', 'value': self._consume().value}
        elif self._match('IDENTIFIER'):
            return self.environment.get(self._consume().value)
        elif self._match('LPAREN'):
            self._consume()
            expr = self.parse_expression()
            if self._match('RPAREN'):
                self._consume()
                return expr
            else:
                raise Exception("Expected ')'")
        return None

    def _match(self, type, value=None):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][0] == type:
            if value is None or self.tokens[self.current_token_index][1] == value:
                return True
        return False






"""-----------------------------------------------------------------------------------------------------------------------------------------"""
# Evaluator
class Evaluator:
    def __init__(self, ast):
        self.ast = ast
        self.environment = {}

    def evaluate(self):
        return self._evaluate(self.ast)


"""-----------------------------------------------------------------------------------------------------------------------------------------"""





#Registries

def _initialize_registries(self):
    return {
        'market_data': {
            'type': 'market_data',
            'elements': {
                'open': {'type': 'price', 'default': 0.0},
                'high': {'type': 'price', 'default': 0.0},
                'low': {'type': 'price', 'default': 0.0},
                'close': {'type': 'price', 'default': 0.0},
                'volume': {'type': 'volume', 'default': 0},
                'hl2': {'type': 'calculation', 'formula': '(high + low) / 2'},
                'hlc3': {'type': 'calculation', 'formula': '(high + low + close) / 3'},
                'hlcc4': {'type': 'calculation', 'formula': '(high + low + close + close) / 4'},
                'ohlc4': {'type': 'calculation', 'formula': '(open + high + low + close) / 4'},
                'symInfoMinMove': {'type': 'number', 'default': 0.01},
                'symInfoMinTick': {'type': 'number', 'default': 0.01},
                'symInfoPointValue': {'type': 'number', 'default': 1.0},
                'symInfoPrefix': {'type': 'string', 'default': ''},
                'symInfoPriceScale': {'type': 'number', 'default': 100},
                'symInfoRoot': {'type': 'string', 'default': ''},
                'symInfoSector': {'type': 'string', 'default': ''},
                'symInfoSession': {'type': 'string', 'default': '24x7'},
                'symInfoShareholders': {'type': 'number', 'default': 0},
                'symInfoSharesOutstandingFloat': {'type': 'number', 'default': 0},
                'symInfoSharesOutstandingTotal': {'type': 'number', 'default': 0}
            }
        },

        'technical_analysis': {
            'type': 'indicators',
            'elements': {
                'taAccDist': {'type': 'volume', 'calculation': 'accumulation_distribution'},
                'taIII': {'type': 'volume', 'calculation': 'intraday_intensity'},
                'taNVI': {'type': 'volume', 'calculation': 'negative_volume_index'},
                'taOBV': {'type': 'volume', 'calculation': 'on_balance_volume'},
                'taPVI': {'type': 'volume', 'calculation': 'positive_volume_index'},
                'taPVT': {'type': 'volume', 'calculation': 'price_volume_trend'},
                'taTR': {'type': 'volatility', 'calculation': 'true_range'},
                'taVWAP': {'type': 'price', 'calculation': 'volume_weighted_average_price'},
                'taWAD': {'type': 'volume', 'calculation': 'williams_accumulation_distribution'},
                'taWVAD': {'type': 'volume', 'calculation': 'weighted_volume_accumulation_distribution'},
                'taAlma': {'type': 'moving_average', 'calculation': 'arnaud_legoux_ma'},
                'taAtr': {'type': 'volatility', 'calculation': 'average_true_range'},
                'taBarsSince': {'type': 'bars', 'calculation': 'bars_since_condition'},
                'taBb': {'type': 'bands', 'calculation': 'bollinger_bands'},
                'taBbw': {'type': 'bands', 'calculation': 'bollinger_bandwidth'},
                'taCci': {'type': 'oscillator', 'calculation': 'commodity_channel_index'},
                'taChange': {'type': 'momentum', 'calculation': 'change'},
                'taCmo': {'type': 'oscillator', 'calculation': 'chande_momentum'},
                'taCog': {'type': 'momentum', 'calculation': 'center_of_gravity'},
                'taCorrelation': {'type': 'statistical', 'calculation': 'correlation'},
                'taCross': {'type': 'pattern', 'calculation': 'cross'},
                'taCrossover': {'type': 'pattern', 'calculation': 'crossover'},
                'taCrossunder': {'type': 'pattern', 'calculation': 'crossunder'},
                'taCum': {'type': 'cumulative', 'calculation': 'cumulative'},
                'taDev': {'type': 'statistical', 'calculation': 'deviation'},
                'taDmi': {'type': 'directional', 'calculation': 'directional_movement_index'},
                'taEma': {'type': 'moving_average', 'calculation': 'exponential_moving_average'},
                'taFalling': {'type': 'trend', 'calculation': 'falling'},
                'taHighest': {'type': 'extremes', 'calculation': 'highest'},
                'taHighestBars': {'type': 'bars', 'calculation': 'highest_bars'},
                'taHma': {'type': 'moving_average', 'calculation': 'hull_moving_average'},
                'taKc': {'type': 'bands', 'calculation': 'keltner_channels'},
                'taKcw': {'type': 'bands', 'calculation': 'keltner_channels_width'},
                'taLinReg': {'type': 'regression', 'calculation': 'linear_regression'},
                'taLowest': {'type': 'extremes', 'calculation': 'lowest'},
                'taLowestBars': {'type': 'bars', 'calculation': 'lowest_bars'},
                'taMacd': {'type': 'momentum', 'calculation': 'moving_average_convergence_divergence'},
                'taMax': {'type': 'statistical', 'calculation': 'maximum'},
                'taMedian': {'type': 'statistical', 'calculation': 'median'},
                'taMfi': {'type': 'volume', 'calculation': 'money_flow_index'},
                'taMin': {'type': 'statistical', 'calculation': 'minimum'},
                'taMode': {'type': 'statistical', 'calculation': 'mode'},
                'taMom': {'type': 'momentum', 'calculation': 'momentum'},
                'taPercentile': {'type': 'statistical', 'calculation': 'percentile'},
                'taPercentRank': {'type': 'statistical', 'calculation': 'percent_rank'},
                'taPivotHigh': {'type': 'pivot', 'calculation': 'pivot_high'},
                'taPivotLow': {'type': 'pivot', 'calculation': 'pivot_low'},
                'taRange': {'type': 'volatility', 'calculation': 'range'},
                'taRising': {'type': 'trend', 'calculation': 'rising'},
                'taRma': {'type': 'moving_average', 'calculation': 'rolling_moving_average'},
                'taRoc': {'type': 'momentum', 'calculation': 'rate_of_change'},
                'taRsi': {'type': 'oscillator', 'calculation': 'relative_strength_index'},
                'taSar': {'type': 'trend', 'calculation': 'parabolic_sar'},
                'taSma': {'type': 'moving_average', 'calculation': 'simple_moving_average'},
                'taStdev': {'type': 'statistical', 'calculation': 'standard_deviation'},
                'taStoch': {'type': 'oscillator', 'calculation': 'stochastic'},
                'taSuperTrend': {'type': 'trend', 'calculation': 'supertrend'},
                'taSwma': {'type': 'moving_average', 'calculation': 'symmetrically_weighted_moving_average'},
                'taTsi': {'type': 'momentum', 'calculation': 'true_strength_index'},
                'taValueWhen': {'type': 'condition', 'calculation': 'value_when'},
                'taVariance': {'type': 'statistical', 'calculation': 'variance'},
                'taVwap': {'type': 'volume', 'calculation': 'volume_weighted_average_price'},
                'taVwma': {'type': 'moving_average', 'calculation': 'volume_weighted_moving_average'},
                'taWma': {'type': 'moving_average', 'calculation': 'weighted_moving_average'},
                'taWpr': {'type': 'oscillator', 'calculation': 'williams_percent_r'}
            }
        },
    'strategy': {
            'type': 'trading',
            'elements': {
                'strategyAccountCurrency': {'type': 'string', 'default': 'USD'},
                'strategyAvgLosingTrade': {'type': 'calculation', 'default': 0.0},
                'strategyAvgLosingTradePercent': {'type': 'calculation', 'default': 0.0},
                'strategyAvgTrade': {'type': 'calculation', 'default': 0.0},
                'strategyAvgTradePercent': {'type': 'calculation', 'default': 0.0},
                'strategyAvgWinningTrade': {'type': 'calculation', 'default': 0.0},
                'strategyAvgWinningTradePercent': {'type': 'calculation', 'default': 0.0},
                'strategyClosedTrades': {'type': 'number', 'default': 0},
                'strategyClosedTradesFirstIndex': {'type': 'number', 'default': 0},
                'strategyEquity': {'type': 'number', 'default': 0.0},
                'strategyEvenTrades': {'type': 'number', 'default': 0},
                'strategyGrossLoss': {'type': 'calculation', 'default': 0.0},
                'strategyGrossLossPercent': {'type': 'calculation', 'default': 0.0},
                'strategyGrossProfit': {'type': 'calculation', 'default': 0.0},
                'strategyGrossProfitPercent': {'type': 'calculation', 'default': 0.0},
                'strategyInitialCapital': {'type': 'number', 'default': 10000.0},
                'strategyLossTrades': {'type': 'number', 'default': 0},
                'strategyMarginLiquidationPrice': {'type': 'price', 'default': 0.0},
                'strategyMaxContractsHeldAll': {'type': 'number', 'default': 0},
                'strategyMaxContractsHeldLong': {'type': 'number', 'default': 0},
                'strategyMaxContractsHeldShort': {'type': 'number', 'default': 0},
                'strategyMaxDrawdown': {'type': 'calculation', 'default': 0.0},
                'strategyMaxDrawdownPercent': {'type': 'calculation', 'default': 0.0},
                'strategyMaxRunup': {'type': 'calculation', 'default': 0.0},
                'strategyMaxRunupPercent': {'type': 'calculation', 'default': 0.0},
                'strategyNetProfit': {'type': 'calculation', 'default': 0.0},
                'strategyNetProfitPercent': {'type': 'calculation', 'default': 0.0},
                'strategyOpenProfit': {'type': 'calculation', 'default': 0.0},
                'strategyOpenProfitPercent': {'type': 'calculation', 'default': 0.0},
                'strategyOpenTrades': {'type': 'number', 'default': 0},
                'strategyOpenTradesCapitalHeld': {'type': 'calculation', 'default': 0.0},
                'strategyPositionAvgPrice': {'type': 'price', 'default': 0.0},
                'strategyPositionEntryName': {'type': 'string', 'default': ''},
                'strategyPositionSize': {'type': 'number', 'default': 0},
                'strategyWinTrades': {'type': 'number', 'default': 0}
            }
        },

        'chart_elements': {
            'type': 'visual',
            'elements': {
                'boxAll': {'type': 'collection', 'items': 'box'},
                'chartBgCol': {'type': 'color', 'default': 'white'},
                'chartFgCol': {'type': 'color', 'default': 'black'},
                'chartIsHeikinAshi': {'type': 'boolean', 'default': false},
                'chartIsKagi': {'type': 'boolean', 'default': false},
                'chartIsLineBreak': {'type': 'boolean', 'default': false},
                'chartIsPnf': {'type': 'boolean', 'default': false},
                'chartIsRange': {'type': 'boolean', 'default': false},
                'chartIsRenko': {'type': 'boolean', 'default': false},
                'chartIsStandard': {'type': 'boolean', 'default': true},
                'chartLeftVisibleBarTime': {'type': 'time', 'default': 0},
                'chartRightVisibleBarTime': {'type': 'time', 'default': 0},
                'labelAll': {'type': 'collection', 'items': 'label'},
                'lineAll': {'type': 'collection', 'items': 'line'},
                'lineFillAll': {'type': 'collection', 'items': 'lineFill'},
                'polylineAll': {'type': 'collection', 'items': 'polyline'},
                'tableAll': {'type': 'collection', 'items': 'table'}
            }
        },



    'time_session': {
            'type': 'temporal',
            'elements': {
                'dayOfMonth': {'type': 'number', 'range': [1, 31]},
                'dayOfWeek': {'type': 'number', 'range': [0, 6]},
                'hour': {'type': 'number', 'range': [0, 23]},
                'minute': {'type': 'number', 'range': [0, 59]},
                'month': {'type': 'number', 'range': [1, 12]},
                'second': {'type': 'number', 'range': [0, 59]},
                'time': {'type': 'timestamp', 'default': 0},
                'timeClose': {'type': 'timestamp', 'default': 0},
                'timeTradingDay': {'type': 'timestamp', 'default': 0},
                'timeNow': {'type': 'timestamp', 'default': 0},
                'weekOfYear': {'type': 'number', 'range': [1, 53]},
                'year': {'type': 'number', 'range': [1900, 2100]},
                'sessionIsFirstBar': {'type': 'boolean', 'default': false},
                'sessionIsFirstBarRegular': {'type': 'boolean', 'default': false},
                'sessionIsLastBar': {'type': 'boolean', 'default': false},
                'sessionIsLastBarRegular': {'type': 'boolean', 'default': false},
                'sessionIsMarket': {'type': 'boolean', 'default': false},
                'sessionIsPostMarket': {'type': 'boolean', 'default': false},
                'sessionIsPreMarket': {'type': 'boolean', 'default': false}
            }
        },

        'symbol_info': {
            'type': 'metadata',
            'elements': {
                'symInfoRecommendationsBuy': {'type': 'number', 'default': 0},
                'symInfoRecommendationsBuyStrong': {'type': 'number', 'default': 0},
                'symInfoRecommendationsDate': {'type': 'timestamp', 'default': 0},
                'symInfoRecommendationsHold': {'type': 'number', 'default': 0},
                'symInfoRecommendationsSell': {'type': 'number', 'default': 0},
                'symInfoRecommendationsSellStrong': {'type': 'number', 'default': 0},
                'symInfoRecommendationsTotal': {'type': 'number', 'default': 0},
                'symInfoTargetPriceAverage': {'type': 'price', 'default': 0.0},
                'symInfoTargetPriceDate': {'type': 'timestamp', 'default': 0},
                'symInfoTargetPriceEstimates': {'type': 'number', 'default': 0},
                'symInfoTargetPriceHigh': {'type': 'price', 'default': 0.0},
                'symInfoTargetPriceLow': {'type': 'price', 'default': 0.0},
                'symInfoTargetPriceMedian': {'type': 'price', 'default': 0.0},
                'symInfoTicker': {'type': 'string', 'default': ''},
                'symInfoTickerId': {'type': 'string', 'default': ''},
                'symInfoTimezone': {'type': 'string', 'default': 'UTC'},
                'symInfoType': {'type': 'string', 'default': ''},
                'symInfoVolumeType': {'type': 'string', 'default': ''}
            }
        },

        'constants': {
            'type': 'constant',
            'elements': {
                'adjustmentDividends': {'type': 'adjustment', 'value': 'dividends'},
                'adjustmentNone': {'type': 'adjustment', 'value': 'none'},
                'adjustmentSplits': {'type': 'adjustment', 'value': 'splits'},
                'alertFreqAll': {'type': 'alert', 'value': 'all'},
                'alertFreqOncePerBar': {'type': 'alert', 'value': 'once_per_bar'},
                'alertFreqOncePerBarClose': {'type': 'alert', 'value': 'once_per_bar_close'},
                'colAqua': {'type': 'color', 'value': '#00FFFF'},
                'colBlack': {'type': 'color', 'value': '#000000'},
                'colBlue': {'type': 'color', 'value': '#0000FF'},
                'colFuchsia': {'type': 'color', 'value': '#FF00FF'},
                'colGray': {'type': 'color', 'value': '#808080'},
                'colGreen': {'type': 'color', 'value': '#008000'},
                'colLime': {'type': 'color', 'value': '#00FF00'},
                'colMaroon': {'type': 'color', 'value': '#800000'},
                'colNavy': {'type': 'color', 'value': '#000080'},
                'colOlive': {'type': 'color', 'value': '#808000'},
                'colOrange': {'type': 'color', 'value': '#FFA500'},
                'colPurple': {'type': 'color', 'value': '#800080'},
                'colRed': {'type': 'color', 'value': '#FF0000'},
                'colSilver': {'type': 'color', 'value': '#C0C0C0'},
                'colTeal': {'type': 'color', 'value': '#008080'},
                'colWhite': {'type': 'color', 'value': '#FFFFFF'},
                'colYellow': {'type': 'color', 'value': '#FFFF00'}
            }
        },


    'currency_constants': {
            'type': 'currency',
            'elements': {
                'currencyAUD': {'type': 'currency', 'value': 'AUD', 'description': 'Australian Dollar'},
                'currencyBTC': {'type': 'currency', 'value': 'BTC', 'description': 'Bitcoin'},
                'currencyCAD': {'type': 'currency', 'value': 'CAD', 'description': 'Canadian Dollar'},
                'currencyCHF': {'type': 'currency', 'value': 'CHF', 'description': 'Swiss Franc'},
                'currencyETH': {'type': 'currency', 'value': 'ETH', 'description': 'Ethereum'},
                'currencyEUR': {'type': 'currency', 'value': 'EUR', 'description': 'Euro'},
                'currencyGBP': {'type': 'currency', 'value': 'GBP', 'description': 'British Pound'},
                'currencyHKD': {'type': 'currency', 'value': 'HKD', 'description': 'Hong Kong Dollar'},
                'currencyINR': {'type': 'currency', 'value': 'INR', 'description': 'Indian Rupee'},
                'currencyJPY': {'type': 'currency', 'value': 'JPY', 'description': 'Japanese Yen'},
                'currencyKRW': {'type': 'currency', 'value': 'KRW', 'description': 'Korean Won'},
                'currencyMYR': {'type': 'currency', 'value': 'MYR', 'description': 'Malaysian Ringgit'},
                'currencyNOK': {'type': 'currency', 'value': 'NOK', 'description': 'Norwegian Krone'},
                'currencyNZD': {'type': 'currency', 'value': 'NZD', 'description': 'New Zealand Dollar'},
                'currencyRUB': {'type': 'currency', 'value': 'RUB', 'description': 'Russian Ruble'},
                'currencySEK': {'type': 'currency', 'value': 'SEK', 'description': 'Swedish Krona'},
                'currencySGD': {'type': 'currency', 'value': 'SGD', 'description': 'Singapore Dollar'},
                'currencyTRY': {'type': 'currency', 'value': 'TRY', 'description': 'Turkish Lira'},
                'currencyUSD': {'type': 'currency', 'value': 'USD', 'description': 'US Dollar'},
                'currencyUSDT': {'type': 'currency', 'value': 'USDT', 'description': 'Tether'},
                'currencyZAR': {'type': 'currency', 'value': 'ZAR', 'description': 'South African Rand'}
            }
        },

        'display_constants': {
            'type': 'display',
            'elements': {
                'displayAll': {'type': 'display', 'value': 'all'},
                'displayDataWindow': {'type': 'display', 'value': 'data_window'},
                'displayNone': {'type': 'display', 'value': 'none'},
                'displayPane': {'type': 'display', 'value': 'pane'},
                'displayPriceScale': {'type': 'display', 'value': 'price_scale'},
                'displayStatusLine': {'type': 'display', 'value': 'status_line'}
            }
        },

        'label_styles': {
            'type': 'style',
            'elements': {
                'labelStyleArrowDown': {'type': 'label_style', 'value': 'arrow_down'},
                'labelStyleArrowUp': {'type': 'label_style', 'value': 'arrow_up'},
                'labelStyleCircle': {'type': 'label_style', 'value': 'circle'},
                'labelStyleCross': {'type': 'label_style', 'value': 'cross'},
                'labelStyleDiamond': {'type': 'label_style', 'value': 'diamond'},
                'labelStyleFlag': {'type': 'label_style', 'value': 'flag'},
                'labelStyleLabelCenter': {'type': 'label_style', 'value': 'label_center'},
                'labelStyleLabelDown': {'type': 'label_style', 'value': 'label_down'},
                'labelStyleLabelLeft': {'type': 'label_style', 'value': 'label_left'},
                'labelStyleLabelLowerLeft': {'type': 'label_style', 'value': 'label_lower_left'},
                'labelStyleLabelLowerRight': {'type': 'label_style', 'value': 'label_lower_right'},
                'labelStyleLabelRight': {'type': 'label_style', 'value': 'label_right'},
                'labelStyleLabelUp': {'type': 'label_style', 'value': 'label_up'},
                'labelStyleLabelUpperLeft': {'type': 'label_style', 'value': 'label_upper_left'},
                'labelStyleLabelUpperRight': {'type': 'label_style', 'value': 'label_upper_right'},
                'labelStyleNone': {'type': 'label_style', 'value': 'none'},
                'labelStyleSquare': {'type': 'label_style', 'value': 'square'},
                'labelStyleTextOutline': {'type': 'label_style', 'value': 'text_outline'},
                'labelStyleTriangleDown': {'type': 'label_style', 'value': 'triangle_down'},
                'labelStyleTriangleUp': {'type': 'label_style', 'value': 'triangle_up'},
                'labelStyleXCross': {'type': 'label_style', 'value': 'xcross'}
            }
        },


      'line_styles': {
            'type': 'style',
            'elements': {
                'lineStyleArrowBoth': {'type': 'line_style', 'value': 'arrow_both'},
                'lineStyleArrowLeft': {'type': 'line_style', 'value': 'arrow_left'},
                'lineStyleArrowRight': {'type': 'line_style', 'value': 'arrow_right'},
                'lineStyleDashed': {'type': 'line_style', 'value': 'dashed'},
                'lineStyleDotted': {'type': 'line_style', 'value': 'dotted'},
                'lineStyleSolid': {'type': 'line_style', 'value': 'solid'},
                'hlineStyleDashed': {'type': 'hline_style', 'value': 'dashed'},
                'hlineStyleDotted': {'type': 'hline_style', 'value': 'dotted'},
                'hlineStyleSolid': {'type': 'hline_style', 'value': 'solid'}
            }
        },

        'position_constants': {
            'type': 'position',
            'elements': {
                'positionBottomCenter': {'type': 'position', 'value': 'bottom_center'},
                'positionBottomLeft': {'type': 'position', 'value': 'bottom_left'},
                'positionBottomRight': {'type': 'position', 'value': 'bottom_right'},
                'positionMiddleCenter': {'type': 'position', 'value': 'middle_center'},
                'positionMiddleLeft': {'type': 'position', 'value': 'middle_left'},
                'positionMiddleRight': {'type': 'position', 'value': 'middle_right'},
                'positionTopCenter': {'type': 'position', 'value': 'top_center'},
                'positionTopLeft': {'type': 'position', 'value': 'top_left'},
                'positionTopRight': {'type': 'position', 'value': 'top_right'}
            }
        },

        'shape_types': {
            'type': 'shape',
            'elements': {
                'shapeArrowDown': {'type': 'shape', 'value': 'arrow_down'},
                'shapeArrowUp': {'type': 'shape', 'value': 'arrow_up'},
                'shapeCircle': {'type': 'shape', 'value': 'circle'},
                'shapeCross': {'type': 'shape', 'value': 'cross'},
                'shapeDiamond': {'type': 'shape', 'value': 'diamond'},
                'shapeFlag': {'type': 'shape', 'value': 'flag'},
                'shapeLabelDown': {'type': 'shape', 'value': 'label_down'},
                'shapeLabelUp': {'type': 'shape', 'value': 'label_up'},
                'shapeSquare': {'type': 'shape', 'value': 'square'},
                'shapeTriangleDown': {'type': 'shape', 'value': 'triangle_down'},
                'shapeTriangleUp': {'type': 'shape', 'value': 'triangle_up'},
                'shapeXCross': {'type': 'shape', 'value': 'xcross'}
            }
        },

        'size_constants': {
            'type': 'size',
            'elements': {
                'sizeAuto': {'type': 'size', 'value': 'auto'},
                'sizeHuge': {'type': 'size', 'value': 'huge'},
                'sizeLarge': {'type': 'size', 'value': 'large'},
                'sizeNormal': {'type': 'size', 'value': 'normal'},
                'sizeSmall': {'type': 'size', 'value': 'small'},
                'sizeTiny': {'type': 'size', 'value': 'tiny'}
            }
        },

        'text_alignment': {
            'type': 'alignment',
            'elements': {
                'textAlignBottom': {'type': 'text_align', 'value': 'bottom'},
                'textAlignCenter': {'type': 'text_align', 'value': 'center'},
                'textAlignLeft': {'type': 'text_align', 'value': 'left'},
                'textAlignRight': {'type': 'text_align', 'value': 'right'},
                'textAlignTop': {'type': 'text_align', 'value': 'top'},
                'textWrapAuto': {'type': 'text_wrap', 'value': 'auto'},
                'textWrapNone': {'type': 'text_wrap', 'value': 'none'}
            }
        },

        'location_types': {
            'type': 'location',
            'elements': {
                'xLocBarIndex': {'type': 'x_location', 'value': 'bar_index'},
                'xLocBarTime': {'type': 'x_location', 'value': 'bar_time'},
                'yLocAboveBar': {'type': 'y_location', 'value': 'above_bar'},
                'yLocBelowBar': {'type': 'y_location', 'value': 'below_bar'},
                'yLocPrice': {'type': 'y_location', 'value': 'price'}
            }
        },

        'matrix_operations': {
            'type': 'matrix',
            'elements': {
                'matrixAddCol': {'type': 'operation', 'function': 'add_column'},
                'matrixAddRow': {'type': 'operation', 'function': 'add_row'},
                'matrixAvg': {'type': 'calculation', 'function': 'average'},
                'matrixCol': {'type': 'access', 'function': 'get_column'},
                'matrixColumns': {'type': 'property', 'function': 'get_column_count'},
                'matrixConcat': {'type': 'operation', 'function': 'concatenate'},
                'matrixCopy': {'type': 'operation', 'function': 'copy'},
                'matrixDet': {'type': 'calculation', 'function': 'determinant'},
                'matrixDiff': {'type': 'calculation', 'function': 'difference'},
                'matrixEigenValues': {'type': 'calculation', 'function': 'eigen_values'},
                'matrixEigenVectors': {'type': 'calculation', 'function': 'eigen_vectors'},
                'matrixElementsCount': {'type': 'property', 'function': 'element_count'},
                'matrixFill': {'type': 'operation', 'function': 'fill'},
                'matrixGet': {'type': 'access', 'function': 'get_element'},
                'matrixInv': {'type': 'calculation', 'function': 'inverse'}
            }
        }
    }

"""---------------------------------------------------------------------------------------------------------------------------------------------"""
#Type Setup and management

def _type_registry(self):
    # Initialize type registry if not exists
    if not hasattr(self, '_registry'):
        self._registry = {
            'arr': {'type': 'array', 'default': []},
            'bool': {'type': 'boolean', 'default': False},
            'box': {'type': 'box', 'default': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}},
            'chartPoint': {'type': 'chartPoint', 'default': {'x': 0, 'y': 0}},
            'col': {'type': 'color', 'default': (0, 0, 0, 255)},
            'const': {'type': 'constant', 'default': None},
            'float': {'type': 'float', 'default': 0.0},
            'int': {'type': 'integer', 'default': 0},
            'label': {'type': 'label', 'default': {'text': '', 'position': {'x': 0, 'y': 0}}},
            'line': {'type': 'line', 'default': {'start': {'x': 0, 'y': 0}, 'end': {'x': 0, 'y': 0}}},
            'lineFill': {'type': 'lineFill', 'default': {'line1': None, 'line2': None, 'color': None}},
            'map': {'type': 'map', 'default': {}},
            'matrx': {'type': 'matrix', 'default': {'value': [[]], 'dimensions': (0, 0)}},
            'polyline': {'type': 'polyline', 'default': {'points': []}},
            'series': {'type': 'series', 'default': {'values': [], 'timeframe': None}},
            'simple': {'type': 'simple', 'default': None},
            'string': {'type': 'string', 'default': ''},
            'table': {'type': 'table', 'default': {'rows': [], 'headers': []}}
        }
    
    return self._type_dec_registry()

def get_type_info(self, type_name):
    registry = self._type_registry()
    return registry.get(type_name)

def register_type(self, type_name, type_info):
    registry = self._type_registry()
    registry[type_name] = type_info

def is_valid_type(self, type_name):
    registry = self._type_registry()
    return type_name in registry








def _type_dec_registry(self):
    return {
        'arr': {
            'type': 'array',
            'validator': lambda x: isinstance(x, list),
            'methods': ['push', 'pop', 'length', 'concat']
        },
        'bool': {
            'type': 'boolean',
            'validator': lambda x: isinstance(x, bool),
            'methods': ['toString', 'valueOf']
        },
        'box': {
            'type': 'box',
            'validator': lambda x: all(key in x for key in ['left', 'top', 'right', 'bottom']),
            'methods': ['getArea', 'getPerimeter', 'contains']
        },
        'chartPoint': {
            'type': 'chartPoint',
            'validator': lambda x: all(key in x for key in ['x', 'y']),
            'methods': ['getX', 'getY', 'setX', 'setY']
        },
        'col': {
            'type': 'color',
            'validator': lambda x: len(x) == 4 and all(0 <= v <= 255 for v in x),
            'methods': ['toHex', 'toRGB', 'toRGBA']
        },
        'const': {
            'type': 'constant',
            'validator': lambda x: True,  # Constants can be any type
            'methods': ['getValue']
        },
        'float': {
            'type': 'float',
            'validator': lambda x: isinstance(x, float),
            'methods': ['round', 'ceil', 'floor']
        },
        'int': {
            'type': 'integer',
            'validator': lambda x: isinstance(x, int),
            'methods': ['toFloat', 'toString', 'abs']
        },
        'label': {
            'type': 'label',
            'validator': lambda x: all(key in x for key in ['text', 'position']),
            'methods': ['setText', 'setPosition', 'getText', 'getPosition']
        },
        'line': {
            'type': 'line',
            'validator': lambda x: all(key in x['points'] for key in ['start', 'end']),
            'methods': ['getLength', 'getSlope', 'getMidpoint']
        },
        'lineFill': {
            'type': 'lineFill',
            'validator': lambda x: all(key in x for key in ['line1', 'line2', 'color']),
            'methods': ['setColor', 'getColor', 'clear']
        },
        'map': {
            'type': 'map',
            'validator': lambda x: isinstance(x, dict),
            'methods': ['get', 'set', 'has', 'delete', 'clear']
        },
        'matrx': {
            'type': 'matrix',
            'validator': lambda x: isinstance(x['value'], list) and len(x['dimensions']) == 2,
            'methods': ['transpose', 'determinant', 'inverse']
        },
        'polyline': {
            'type': 'polyline',
            'validator': lambda x: isinstance(x['points'], list),
            'methods': ['addPoint', 'removePoint', 'getLength']
        },
        'series': {
            'type': 'series',
            'validator': lambda x: isinstance(x['values'], list),
            'methods': ['sum', 'average', 'median']
        },
        'simple': {
            'type': 'simple',
            'validator': lambda x: True,  # Simple types can be any value
            'methods': ['toString', 'valueOf']
        },
        'string': {
            'type': 'string',
            'validator': lambda x: isinstance(x, str),
            'methods': ['length', 'concat', 'substring']
        },
        'table': {
            'type': 'table',
            'validator': lambda x: isinstance(x['rows'], list) and isinstance(x['headers'], list),
            'methods': ['addRow', 'deleteRow', 'getCell']
        }
    }



"""---------------------------------------------------------------------------------------------------------------------------------------------"""

# Evaluate Syntax Classes


def _evaluate_builtin_variable(self, node):
    # Market Data Variables
        if node['value'] in ['open', 'high', 'low', 'close', 'volume']:
            return self.environment.get(node['value'], 0)

        # Bar State Variables 
        elif node['value'] in ['barIndex', 'barStateIsConfirmed', 'barStateIsFirst', 'barStateIsHistory', 'barStateIsLast', 
                              'barStateIsLastConfirmedHistory', 'barStateIsNew', 'barStateIsRealtime']:
            return self.environment.get(node['value'], False)

        # Chart Variables
        elif node['value'] in ['boxAll', 'chartBgCol', 'chartFgCol', 'chartIsHeikinAshi', 'chartIsKagi', 'chartIsLineBreak',
                              'chartIsPnf', 'chartIsRange', 'chartIsRenko', 'chartIsStandard', 'chartLeftVisibleBarTime',
                              'chartRightVisibleBarTime']:
            return self.environment.get(node['value'], None)

        # Time Variables
        elif node['value'] in ['dayOfMonth', 'dayOfWeek', 'hour', 'minute', 'month', 'second', 'time', 'timeClose',
                              'timeTradingDay', 'timeNow', 'weekOfYear', 'year']:
            return self.environment.get(node['value'], 0)

        # Dividend and Earnings Variables
        elif node['value'] in ['dividendsFutureAmount', 'dividendsFutureExDate', 'dividendsFuturePayDate', 'earningsFutureEps',
                              'earningsFuturePeriodEndTime', 'earningsFutureRevenue', 'earningsFutureTime']:
            return self.environment.get(node['value'], None)

        # Price Calculation Variables
        elif node['value'] in ['hl2', 'hlc3', 'hlcc4', 'ohlc4']:
            return self._calculate_price_averages(node['value'])

        # UI Element Variables
        elif node['value'] in ['labelAll', 'lastBarIndex', 'lastBarTime', 'lineAll', 'lineFillAll', 'polylineAll', 'tableAll']:
            return self.environment.get(node['value'], [])

        # Session State Variables
        elif node['value'] in ['sessionIsFirstBar', 'sessionIsFirstBarRegular', 'sessionIsLastBar', 'sessionIsLastBarRegular',
                              'sessionIsMarket', 'sessionIsPostMarket', 'sessionIsPreMarket']:
            return self.environment.get(node['value'], False)

        # Strategy Variables
        elif node['value'].startswith('strategy'):
            return self.environment.get(node['value'], 0)

        # Symbol Info Variables
        elif node['value'].startswith('symInfo'):
            return self.environment.get(node['value'], None)

        # Technical Analysis Variables
        elif node['value'] in ['taAccDist', 'taIII', 'taNVI', 'taOBV', 'taPVI', 'taPVT', 'taTR', 'taVWAP', 'taWAD', 'taWVAD']:
            return self.environment.get(node['value'], 0)

        # Timeframe Variables
        elif node['value'] in ['timeframeIsDaily', 'timeframeIsDWM', 'timeframeIsIntraday', 'timeframeIsMinutes',
                              'timeframeIsMonthly', 'timeframeIsSeconds', 'timeframeIsTicks', 'timeframeIsWeekly',
                              'timeframeMainPeriod', 'timeframeMultiplier', 'timeframePeriod']:
            return self.environment.get(node['value'], False)

        # Special Values
        elif node['value'] == 'na':
            return None

        return None




#builtin_functions

def _evaluate_builtin_function(self, node):
        args = [self._evaluate(arg) for arg in node['arguments']]

    # Alert and Notification Functions
        if node['name'] == 'alertFunc':
            print(f"ALERT: {args[0]}")
            return None
        elif node['name'] == 'alertConditionFunc':
            return args[0] and args[1]
        elif node['name'] == 'logErrorFunc':
            print(f"ERROR: {args[0]}")
            return None
        elif node['name'] == 'logInfoFunc':
            print(f"INFO: {args[0]}")
            return None
        elif node['name'] == 'logWarningFunc':
            print(f"WARNING: {args[0]}")
            return None

        # Array Functions
        elif node['name'] in ['arrAbs', 'arrAvg', 'arrBinarySearch', 'arrBinarySearchLeftmost', 'arrBinarySearchRightmost', 'arrClear', 'arrConcat', 'arrCopy', 'arrCovariance', 'arrEvery', 'arrFill', 'arrFirst', 'arrFrom', 'arrGet', 'arrIncludes', 'arrIndexOf', 'arrInsert', 'arrJoin', 'arrLast', 'arrLastIndexOf', 'arrMax', 'arrMedian', 'arrMin', 'arrMode', 'arrNewBool', 'arrNewBox', 'aryNewCol', 'arrNewFloat', 'arrNewInt', 'arrNewLabel', 'arrNewLine', 'arrNewLineFill', 'arrNewString', 'arrNewTable', 'arrNewType', 'arrPercentileLinearInterpolation', 'arrPercentileNearestRank', 'arrPercentRank', 'arrPop', 'arrPush', 'arrRange', 'arrRemove', 'arrReverse', 'arrSet', 'arrShift', 'arrSize', 'arrSlice', 'arrSome', 'arrSort', 'arrSortIndices', 'arrStandardize', 'arrStdev', 'arrSum', 'arrUnshift', 'arrVariance']:
            return self._handle_array_operation(node['name'], args)

        # Box Functions
        elif node['name'] in ['boxFunc', 'boxCopyFunc', 'boxDeleteFunc','boxGetBottomFunc', 'boxGetLeftFunc','boxGetRightFunc', 'boxGetTopFunc', 'boxNewFunc','boxSetBgColFunc', 'boxSetBorderColFunc','boxSetBorderStyleFunc', 'boxSetBorderWidthFunc','boxSetBottomFunc', 'boxSetBottomRightPointFunc','boxSetExtendFunc', 'boxSetLeftFunc','boxSetLeftTopFunc', 'boxSetRightFunc', 'boxSetRightBottomFunc','boxSetTextFunc','boxSetTextColFunc', 'boxSetTextFontFamilyFunc', 'boxSetTextHAlignFunc','boxSetTextSizeFunc','boxSetTextVAlignFunc', 'boxSetTextWrapFunc', 'boxSetTopFunc','boxSetTopLeftPointFunc','chartPointCopyFunc', 'chartPointFromIndexFunc',]:
            return self._handle_box_operation(node['name'], args)

        # Chart Functions
        elif node['name'] in ['chartPointCopyFunc', 'chartPointFromIndexFunc', 'chartPointFromTimeFunc',
                             'chartPointNewFunc', 'chartPointNowFunc']:
            return self._handle_chart_operation(node['name'], args)

        # Weird Functions
        elif node['name'] in ['dayOfMonthFunc', 'dayOfWeekFunc', 'fillFunc','fixNanFunc', 'floatFunc','hLineFunc', 'hourFunc', 'indicatorFunc','maxBarsBackFunc', 'minuteFunc', 'monthFunc', 'naFunc','nzFunc', 'polylineDeleteFunc','polylineNewFunc', 'requestCurrencyRateFunc', 'requestDividendsFunc','requestEarningsFunc','requestEconomicFunc', 'requestFinancialFunc', 'requestQuandlFunc', 'requestSecurityFunc','requestSecurityLowerTfFunc', 'requestSeedFunc', 'requestSplitsFunc', 'runtimeErrorFunc','secondFunc','barColFunc','bgColFunc', 'boolFunc']:
            return self._handle_weird_operation(node['name'], args)

        # Color Functions
        elif node['name'] in ['colFunc', 'colBFunc', 'colFromGradientFunc', 'colGFunc', 'colNewFunc','colRFunc', 'colRgbFunc', 'colTFunc']:
            return self._handle_color_operation(node['name'], args)

        # Input Functions
        elif node['name'] in ['inputFunc','inputBoolFunc', 'inputColFunc', 'inputEnumFunc', 'inputFloatFunc','inputIntFunc','inputPriceFunc', 'inputSessionFunc', 'inputSourceFunc', 'inputStringFunc','inputSymbolFunc','inputTextAreaFunc', 'inputTimeFunc', 'inputTimeFrameFunc', 'intFunc']:
            return self._handle_input_operation(node['name'], args)

        # Label Functions
        elif node['name'] in ['labelFunc','labelCopyFunc', 'labelDeleteFunc', 'labelGetTextFunc', 'labelGetXFunc', 'labelGetYFunc','labelNewFunc', 'labelSetColFunc', 'labelSetPointFunc', 'labelSetSizeFunc', 'labelSetStyleFunc','labelSetTextFunc', 'labelSetTextFontFamilyFunc', 'labelSetTextAlignFunc', 'labelSetTextColFunc','labelSetToolTipFunc', 'labelSetXFunc', 'labelSetXLocFunc', 'labelSetXYFunc', 'labelSetYFunc','labelSetYLocFunc']:
            return self._handle_label_operation(node['name'], args)

        # Line Functions
        elif node['name'] in ['libraryFunc', 'lineFunc', 'lineCopyFunc', 'lineDeleteFunc','lineGetPriceFunc', 'lineGetX1Func','lineGetX2Func', 'lineGetY1Func', 'lineGetY2Func','lineNewFunc', 'lineSetColFunc', 'lineSetExtendFunc','lineSetFirstPointFunc','lineSetSecondPointFunc', 'lineSetStyleFunc', 'lineSetWidthFunc', 'lineSetX1Func','lineSetX2Func', 'lineSetXLocFunc', 'lineSetXY1Func', 'lineSetXY2Func', 'lineSetY1Func','lineSetY2Func', 'lineFillFunc', 'lineFillDeleteFunc', 'lineFillGetLine1Func','lineFillGetLine2Func', 'lineFillNewFunc', 'lineFillSetColFunc']:
            return self._handle_line_operation(node['name'], args)

        # log Functions
        elif node['name'] in ['logErrorFunc','logInfoFunc', 'logWarningFunc']:
            return self._handle_log_operation(node['name'], args)

        # map Functions
        elif node['name'] in ['mapClearFunc', 'mapContainsFunc', 'mapCopyFunc','mapGetFunc', 'mapKeysFunc', 'mapNewTypeFunc','mapPutFunc', 'mapPutAllFunc','mapRemoveFunc', 'mapSizeFunc', 'mapValuesFunc']:
            return self._handle_map_operation(node['name'], args)

        # Math Functions
        elif node['name'] in ['mathAbsFunc', 'mathAcosFunc','mathAsinFunc', 'mathAtanFunc', 'mathAvgFunc', 'mathCeilFunc','mathCosFunc','mathExpFunc', 'mathFloorFunc', 'mathLogFunc', 'mathLog10Func', 'mathMaxFunc','mathMinFunc', 'mathPowFunc', 'mathRandomFunc', 'mathRoundFunc', 'mathRoundToMinTickFunc','mathSignFunc', 'mathSinFunc', 'mathSqrtFunc', 'mathSumFunc', 'mathTanFunc','mathToDegreesFunc', 'mathToRadiansFunc']:
            return self._handle_math_operation(node['name'], args)

        # Matrix Functions
        elif node['name'] in ['matrixAddColFunc', 'matrixAddRowFunc','matrixAvgFunc', 'matrixColFunc', 'matrixColumnsFunc', 'matrixConcatFunc', 'matrixCopyFunc','matrixDetFunc', 'matrixDiffFunc', 'matrixEigenValuesFunc', 'matrixEigenVectorsFunc','matrixElementsCountFunc', 'matrixFillFunc', 'matrixGetFunc', 'matrixInvFunc','matrixIsAntiDiagonalFunc', 'matrixIsAntiSymmetricFunc', 'matrixIsBinaryFunc','matrixIsDiagonalFunc','matrixIsIdentityFunc', 'matrixIsSquareFunc', 'matrixIsStochasticFunc','matrixIsSymmetricFunc','matrixIsTriangularFunc', 'matrixIsZeroFunc', 'matrixKronFunc','matrixMaxFunc', 'matrixMedianFunc','matrixMinFunc', 'matrixModeFunc', 'matrixMultFunc','matrixNewTypeFunc', 'matrixPinvFunc', 'matrixPowFunc','matrixRankFunc', 'matrixRemoveColFunc','matrixRemoveRowFunc', 'matrixReshapeFunc', 'matrixReverseFunc','matrixRowFunc','matrixRowsFunc', 'matrixSetFunc', 'matrixSortFunc', 'matrixSubMatrixFunc', 'matrixSumFunc','matrixSwapColumnsFunc', 'matrixSwapRowsFunc', 'matrixTraceFunc', 'matrixTransposeFunc']:
            return self._handle_matrix_operation(node['name'], args)

        # str Functions
        elif node['name'] in ['strContainsFunc', 'strEndsWithFunc', 'strFormatFunc', 'strFormatTimeFunc','strLengthFunc', 'strLowerFunc', 'strMatchFunc', 'strPosFunc', 'strRepeatFunc','strReplaceFunc', 'strReplaceAllFunc', 'strSplitFunc', 'strStartsWithFunc', 'strSubstringFunc','strToNumberFunc', 'strToStringFunc', 'strTrimFunc', 'strUpperFunc']:
            return self._handle_str_operation(node['name'], args)


        # Strategy Functions
        elif node['name'] in ['strategyFunc','strategyCancelFunc', 'strategyCancelAllFunc', 'strategyCloseFunc', 'strategyCloseAllFunc','strategyClosedTradesCommissionFunc', 'strategyClosedTradesEntryBarIndexFunc','strategyClosedTradesEntryCommentFunc', 'strategyClosedTradesEntryIdFunc','strategyClosedTradesEntryPriceFunc','strategyClosedTradesEntryTimeFunc','strategyClosedTradesExitBarIndexFunc', 'strategyClosedTradesExitCommentFunc','strategyClosedTradesExitIdFunc', 'strategyClosedTradesExitPriceFunc','strategyClosedTradesExitTimeFunc','strategyClosedTradesMaxDrawdownFunc','strategyClosedTradesMaxDrawdownPercentFunc', 'strategyClosedTradesMaxRunupFunc','strategyClosedTradesMaxRunupPercentFunc', 'strategyClosedTradesProfitFunc','strategyClosedTradesProfitPercentFunc','strategyClosedTradesSizeFunc','strategyConver,ToAccountFunc', 'strategyConvertToSymbolFunc', 'strategyDefaultEntryQtyFunc','strategyEntryFunc', 'strategyExitFunc', 'strategyOpenTradesCommissionFunc','strategyOpenTradesEntryBarIndexFunc','strategyOpenTradesEntryCommentFunc','strategyOpenTradesEntryIdFunc', 'strategyOpenTradesEntryPriceFunc','strategyOpenTradesEntryTimeFunc', 'strategyOpenTradesMaxDrawdownFunc','strategyOpenTradesMaxDrawdownPercentFunc','strategyOpenTradesMaxRunupFunc','strategyOpenTradesMaxRunupPercentFunc', 'strategyOpenTradesProfitFunc','strategyOpenTradesProfitPercentFunc', 'strategyOpenTradesSizeFunc', 'strategyOrderFunc','strategyRiskAllowEntryInFunc','strategyRiskMaxConsLossDaysFunc', 'strategyRiskMaxDrawdownFunc','strategyRiskMaxIntradayFilledOrdersFunc','strategyRiskMaxIntradayLossFunc','strategyRiskMaxPositionSizeFunc']:
            return self._handle_strategy_operation(node['name'], args)

        # Time Functions
        elif node['name'] in ['symInfoPrefixFunc', 'symInfoTickerFunc', 'timeFunc','timeCloseFunc', 'timeframeChangeFunc','timeframeFromSecondsFunc', 'timeframeInSecondsFunc','timestampFunc', 'weekOfYearFunc', 'yearFunc']:
            return self._handle_time_operation(node['name'], args)

        # Original functions remain unchanged
        elif node['name'] == 'sma':
            return sum(args[0][-args[1]:]) / args[1]
        elif node['name'] == 'ema':
            k = 2 / (args[1] + 1)
            ema = args[0][0]
            for price in args[0][1:]:
                ema = price * k + ema * (1 - k)
            return ema
        elif node['name'] == 'rsi':
            gains = [args[0][i] - args[0][i - 1] for i in range(1, len(args[0])) if args[0][i] > args[0][i - 1]]
            losses = [-args[0][i] + args[0][i - 1] for i in range(1, len(args[0])) if args[0][i] < args[0][i - 1]]
            avg_gain = sum(gains) / args[1]
            avg_loss = sum(losses) / args[1]
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            return 100 - (100 / (1 + rs))

        return None


#type_declaration

def _evaluate_type_declaration(self, node):
    args = [self._evaluate(arg) for arg in node['arguments']]
    
    # Type Declaration Functions
    if node['name'] == 'arr':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'bool':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'box':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'chartPoint':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'col':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'const':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'float':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'int':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'label':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'line':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'lineFill':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'map':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'matrx':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'polyline':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'series':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'simple':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'string':
        return self._handle_type_declaration(node['name'], args)
    elif node['name'] == 'table':
        return self._handle_type_declaration(node['name'], args)

    return None




#constants

def _evaluate_constant(self, node):
    constants = {
        'showStyleArea': 1,
        'showStyleAreaBr': 2,
        'showStyleCircles': 3,
        'showStyleColumns': 4,
        'showStyleCross': 5,
        'showStyleHistogram': 6,
        'showStyleLine': 7,
        'showStyleLineBr': 8,
        'showStyleStepLine': 9,
        'showStyleStepLineDiamond': 10,
        'showStyleStepLineBr': 11,
        'positionBottomCenter': 12,
        'positionBottomLeft': 13,
        'positionBottomRight': 14,
        'positionMiddleCenter': 15,
        'positionMiddleLeft': 16,
        'positionMiddleRight': 17,
        'positionTopCenter': 18,
        'positionTopLeft': 19,
        'positionTopRight': 20,
        'scaleLeft': 21,
        'scaleNone': 22,
        'scaleRight': 23,
        'sessionExtended': 24,
        'sessionRegular': 25,
        'settlementAsCloseInherit': 26,
        'settlementAsCloseOff': 27,
        'settlementAsCloseOn': 28,
        'shapeArrowDown': 29,
        'shapeArrowUp': 30,
        'shapeCircle': 31,
        'shapeCross': 32,
        'shapeDiamond': 33,
        'shapeFlag': 34,
        'shapeLabelDown': 35,
        'shapeLabelUp': 36,
        'shapeSquare': 37,
        'shapeTriangleDown': 38,
        'shapeTriangleUp': 39,
        'shapeXCross': 40,
        'sizeAuto': 41,
        'sizeHuge': 42,
        'sizeLarge': 43,
        'sizeNormal': 44,
        'sizeSmall': 45,
        'sizeTiny': 46,
        'splitsDenominator': 47,
        'splitsNumerator': 48,
        'strategyCash': 49,
        'strategyCommissionCashPerContract': 50,
        'strategyCommissionCashPerOrder': 51,
        'strategyCommissionPercent': 52,
        'strategyDirectionAll': 53,
        'strategyDirectionLong': 54,
        'strategyDirectionShort': 55,
        'strategyFixed': 56,
        'strategyLong': 57,
        'strategyOcaCancel': 58,
        'strategyOcaNone': 59,
        'strategyOcaReduce': 60,
        'strategyPercentOfEquity': 61,
        'strategyShort': 62,
        'textAlignBottom': 63,
        'textAlignCenter': 64,
        'textAlignLeft': 65,
        'textAlignRight': 66,
        'textAlignTop': 67,
        'textWrapAuto': 68,
        'textWrapNone': 69,
        'trueValue': True,
        'falseValue': False,
        'xLocBarIndex': 70,
        'xLocBarTime': 71,
        'yLocAboveBar': 72,
        'yLocBelowBar': 73,
        'yLocPrice': 74,
        'adjustmentDividends': 75,
        'adjustmentNone': 76,
        'adjustmentSplits': 77,
        'alertFreqAll': 78,
        'alertFreqOncePerBar': 79,
        'alertFreqOncePerBarClose': 80,
        'backAdjustmentInherit': 81,
        'backAdjustmentOff': 82,
        'backAdjustmentOn': 83,
        'barMergeGapsOff': 84,
        'barMergeGapsOn': 85,
        'barMergeLookaheadOff': 86,
        'barMergeLookaheadOn': 87,
        'colAqua': '#00FFFF',
        'colBlack': '#000000',
        'colBlue': '#0000FF',
        'colFuchsia': '#FF00FF',
        'colGray': '#808080',
        'colGreen': '#008000',
        'colLime': '#00FF00',
        'colMaroon': '#800000',
        'colNavy': '#000080',
        'colOlive': '#808000',
        'colOrange': '#FFA500',
        'colPurple': '#800080',
        'colRed': '#FF0000',
        'colSilver': '#C0C0C0',
        'colTeal': '#008080',
        'colWhite': '#FFFFFF',
        'colYellow': '#FFFF00',
        'currencyAUD': 'AUD',
        'currencyBTC': 'BTC',
        'currencyCAD': 'CAD',
        'currencyCHF': 'CHF',
        'currencyETH': 'ETH',
        'currencyEUR': 'EUR',
        'currencyGBP': 'GBP',
        'currencyHKD': 'HKD',
        'currencyINR': 'INR',
        'currencyJPY': 'JPY',
        'currencyKRW': 'KRW',
        'currencyMYR': 'MYR',
        'currencyNOK': 'NOK',
        'currencyNone': '',
        'currencyNZD': 'NZD',
        'currencyRUB': 'RUB',
        'currencySEK': 'SEK',
        'currencySGD': 'SGD',
        'currencyTRY': 'TRY',
        'currencyUSD': 'USD',
        'currencyUSDT': 'USDT',
        'currencyZAR': 'ZAR',
        'dayOfWeekFriday': 5,
        'dayOfWeekMonday': 1,
        'dayOfWeekSaturday': 6,
        'dayOfWeekSunday': 0,
        'dayOfWeekThursday': 4,
        'dayOfWeekTuesday': 2,
        'dayOfWeekWednesday': 3,
        'mathE': 2.718281828459045,
        'mathPi': 3.141592653589793,
        'mathPhi': 1.618033988749895,
        'mathRPhi': 0.618033988749895
    }
    
    return constant.get(node['value'])






#Keyword

def _evaluate_keyword(self, node):
    args = [self._evaluate(arg) for arg in node['arguments']]

    # Control Flow Keywords
    if node['name'] == 'ifCond':
        return self._handle_keyword_operation('ifCond', args)
    elif node['name'] == 'forLoop':
        return self._handle_keyword_operation('forLoop', args)
    elif node['name'] == 'forInLoop':
        return self._handle_keyword_operation('forInLoop', args)
    elif node['name'] == 'whileLoop':
        return self._handle_keyword_operation('whileLoop', args)
    elif node['name'] == 'switchCase':
        return self._handle_keyword_operation('switchCase', args)

    # Logical Operators
    elif node['name'] == 'andOp':
        return self._handle_keyword_operation('andOp', args)
    elif node['name'] == 'orOp':
        return self._handle_keyword_operation('orOp', args)
    elif node['name'] == 'notOp':
        return self._handle_keyword_operation('notOp', args)

    # Variable Declaration
    elif node['name'] == 'let':
        return self._handle_keyword_operation('let', args)
    elif node['name'] == 'letip':
        return self._handle_keyword_operation('letip', args)

    # Type System
    elif node['name'] == 'typeDef':
        return self._handle_keyword_operation('typeDef', args)
    elif node['name'] == 'enumType':
        return self._handle_keyword_operation('enumType', args)

    # Module System
    elif node['name'] == 'importFunc':
        return self._handle_keyword_operation('importFunc', args)
    elif node['name'] == 'exportFunc':
        return self._handle_keyword_operation('exportFunc', args)
    elif node['name'] == 'methodFunc':
        return self._handle_keyword_operation('methodFunc', args)

    return None




"""---------------------------------------------------------------------------------------------------------------------------------------------"""




# Calculation
def _calculate_price_averages(self, calc_type):
    if calc_type == 'hl2' and all(x in self.environment for x in ['high', 'low']):
        return (self.environment['high'] + self.environment['low']) / 2
    elif calc_type == 'hlc3' and all(x in self.environment for x in ['high', 'low', 'close']):
        return (self.environment['high'] + self.environment['low'] + self.environment['close']) / 3
    elif calc_type == 'hlcc4' and all(x in self.environment for x in ['high', 'low', 'close']):
        return (self.environment['high'] + self.environment['low'] + 2 * self.environment['close']) / 4
    elif calc_type == 'ohlc4' and all(x in self.environment for x in ['open', 'high', 'low', 'close']):
        return (self.environment['open'] + self.environment['high'] + self.environment['low'] + self.environment['close']) / 4
    return None


def _calculate_technical_indicators(self):
    """Calculates all technical indicators"""
    close = self.market_data['close']
    volume = self.market_data['volume']
    high = self.market_data['high']
    low = self.market_data['low']

    # Accumulation/Distribution
    self.environment['taAccDist'] = sum(
        ((close[i] - low[i]) - (high[i] - close[i])) / (high[i] - low[i]) * volume[i] 
        for i in range(len(close))
    )

    # Intraday Intensity Index
    self.environment['taIII'] = (2 * close[-1] - high[-1] - low[-1]) / (high[-1] - low[-1]) * volume[-1]

    # On-Balance Volume
    obv = 0
    for i in range(1, len(close)):
        if close[i] > close[i-1]:
            obv += volume[i]
        elif close[i] < close[i-1]:
            obv -= volume[i]
    self.environment['taOBV'] = obv

    # True Range
    tr = []
    for i in range(1, len(close)):
        tr.append(max(
            high[i] - low[i],
            abs(high[i] - close[i-1]),
            abs(low[i] - close[i-1])
        ))
    self.environment['taTR'] = tr[-1] if tr else 0

    # VWAP
    self.environment['taVWAP'] = sum(close * volume) / sum(volume) if volume else 0

def _calculate_strategy_metrics(self):
    """Calculates all strategy performance metrics"""
    trades = self.trades  # Assuming we have a trades list
    
    if trades:
        profits = [t['profit'] for t in trades if t['profit'] > 0]
        losses = [t['profit'] for t in trades if t['profit'] < 0]
        
        self.environment.update({
            'strategyAvgTrade': sum(t['profit'] for t in trades) / len(trades),
            'strategyAvgWinningTrade': sum(profits) / len(profits) if profits else 0,
            'strategyAvgLosingTrade': sum(losses) / len(losses) if losses else 0,
            'strategyNetProfit': sum(t['profit'] for t in trades),
            'strategyWinTrades': len(profits),
            'strategyLossTrades': len(losses)
        })

def _calculate_price_aggregates(self):
    """Calculates price aggregates"""
    if self.market_data['high']:
        high = self.market_data['high'][-1]
        low = self.market_data['low'][-1]
        close = self.market_data['close'][-1]
        open_price = self.market_data['open'][-1]
        
        self.environment.update({
            'hl2': (high + low) / 2,
            'hlc3': (high + low + close) / 3,
            'hlcc4': (high + low + 2 * close) / 4,
            'ohlc4': (open_price + high + low + close) / 4
        })

def _calculate_session_states(self):
    """Determines session states based on current time"""
    current_hour = self.current_time.hour
    current_minute = self.current_time.minute
    
    self.environment.update({
        'sessionIsMarket': 9 <= current_hour < 16,
        'sessionIsPreMarket': 4 <= current_hour < 9,
        'sessionIsPostMarket': 16 <= current_hour < 20,
        'sessionIsFirstBar': current_hour == 9 and current_minute == 30,
        'sessionIsLastBar': current_hour == 16 and current_minute == 0
    })

def _calculate_timeframe_states(self):
    """Sets timeframe states based on current configuration"""
    period_minutes = self.environment['timeframePeriod']
    
    self.environment.update({
        'timeframeIsDaily': period_minutes == 1440,
        'timeframeIsWeekly': period_minutes == 10080,
        'timeframeIsMonthly': period_minutes == 43200,
        'timeframeIsMinutes': period_minutes < 1440,
        'timeframeIsIntraday': period_minutes < 1440,
        'timeframeIsDWM': period_minutes >= 1440
    })

def update_all_calculations(self):
    """Updates all calculated values"""
    self._calculate_technical_indicators()
    self._calculate_strategy_metrics()
    self._calculate_price_aggregates()
    self._calculate_session_states()
    self._calculate_timeframe_states()

def _calculate_market_data(self):
    """Market data calculations"""
    if self.market_data['close']:
        self.environment.update({
            'open': self.market_data['open'][-1],
            'high': self.market_data['high'][-1],
            'low': self.market_data['low'][-1],
            'close': self.market_data['close'][-1],
            'volume': self.market_data['volume'][-1]
        })

def _calculate_bar_states(self):
    """Bar state calculations"""
    current_index = len(self.market_data['close']) - 1
    self.environment.update({
        'barIndex': current_index,
        'barStateIsConfirmed': current_index < len(self.market_data['close']) - 1,
        'barStateIsFirst': current_index == 0,
        'barStateIsLast': current_index == len(self.market_data['close']) - 1,
        'barStateIsNew': self.is_new_bar,
        'barStateIsRealtime': self.is_realtime
    })

def _calculate_time_components(self):
    """Time component calculations"""
    current_time = self.current_time
    self.environment.update({
        'dayOfMonth': current_time.day,
        'dayOfWeek': current_time.weekday() + 1,
        'hour': current_time.hour,
        'minute': current_time.minute,
        'month': current_time.month,
        'second': current_time.second,
        'time': current_time.timestamp(),
        'timeClose': (current_time + timedelta(minutes=1)).timestamp(),
        'timeTradingDay': current_time.replace(hour=0, minute=0, second=0).timestamp(),
        'timeNow': current_time.timestamp(),
        'weekOfYear': current_time.isocalendar()[1],
        'year': current_time.year
    })

def _calculate_price_components(self):
    """Price component calculations"""
    if self.market_data['close']:
        high = self.market_data['high'][-1]
        low = self.market_data['low'][-1]
        close = self.market_data['close'][-1]
        open_price = self.market_data['open'][-1]
        
        self.environment.update({
            'hl2': (high + low) / 2,
            'hlc3': (high + low + close) / 3,
            'hlcc4': (high + low + 2 * close) / 4,
            'ohlc4': (open_price + high + low + close) / 4
        })

def _calculate_technical_indicators(self):
    """Technical indicator calculations"""
    if len(self.market_data['close']) > 1:
        close = np.array(self.market_data['close'])
        volume = np.array(self.market_data['volume'])
        high = np.array(self.market_data['high'])
        low = np.array(self.market_data['low'])

        # Accumulation/Distribution Line
        clv = ((close - low) - (high - close)) / (high - low)
        ad = (clv * volume).cumsum()
        
        # On-Balance Volume
        obv = np.zeros_like(close)
        obv[1:] = np.where(close[1:] > close[:-1], volume[1:], 
                          np.where(close[1:] < close[:-1], -volume[1:], 0)).cumsum()
        
        # True Range
        tr = np.maximum(high - low, 
                       np.maximum(abs(high - np.roll(close, 1)), 
                                abs(low - np.roll(close, 1))))
        
        # VWAP
        vwap = (close * volume).cumsum() / volume.cumsum()
        
        self.environment.update({
            'taAccDist': ad[-1],
            'taOBV': obv[-1],
            'taTR': tr[-1],
            'taVWAP': vwap[-1],
            'taIII': (2 * close[-1] - high[-1] - low[-1]) / (high[-1] - low[-1]) * volume[-1]
        })

def _calculate_strategy_metrics(self):
    """Strategy metrics calculations"""
    if self.trades:
        trades_array = np.array([t['profit'] for t in self.trades])
        winning_trades = trades_array[trades_array > 0]
        losing_trades = trades_array[trades_array < 0]
        
        initial_capital = self.environment['strategyInitialCapital']
        current_equity = initial_capital + trades_array.sum()
        
        self.environment.update({
            'strategyNetProfit': trades_array.sum(),
            'strategyNetProfitPercent': (trades_array.sum() / initial_capital) * 100,
            'strategyAvgTrade': trades_array.mean(),
            'strategyAvgWinningTrade': winning_trades.mean() if len(winning_trades) > 0 else 0,
            'strategyAvgLosingTrade': losing_trades.mean() if len(losing_trades) > 0 else 0,
            'strategyWinTrades': len(winning_trades),
            'strategyLossTrades': len(losing_trades),
            'strategyEquity': current_equity
        })

def _calculate_session_states(self):
    """Session state calculations"""
    current_time = self.current_time
    market_open = current_time.replace(hour=9, minute=30)
    market_close = current_time.replace(hour=16, minute=0)
    pre_market_open = current_time.replace(hour=4, minute=0)
    post_market_close = current_time.replace(hour=20, minute=0)
    
    self.environment.update({
        'sessionIsMarket': market_open <= current_time < market_close,
        'sessionIsPreMarket': pre_market_open <= current_time < market_open,
        'sessionIsPostMarket': market_close <= current_time < post_market_close,
        'sessionIsFirstBar': current_time == market_open,
        'sessionIsLastBar': current_time == market_close
    })

def _calculate_timeframe_states(self):
    """Timeframe state calculations"""
    period_minutes = self.environment['timeframePeriod']
    
    self.environment.update({
        'timeframeIsDaily': period_minutes == 1440,
        'timeframeIsWeekly': period_minutes == 10080,
        'timeframeIsMonthly': period_minutes == 43200,
        'timeframeIsMinutes': period_minutes < 1440,
        'timeframeIsSeconds': period_minutes < 1,
        'timeframeIsTicks': period_minutes == 0,
        'timeframeIsIntraday': period_minutes < 1440,
        'timeframeIsDWM': period_minutes >= 1440,
        'timeframeMainPeriod': self._get_timeframe_period_string(period_minutes),
        'timeframeMultiplier': self._get_timeframe_multiplier(period_minutes)
    })

def _get_timeframe_period_string(self, minutes):
    """Helper method to get timeframe period string"""
    if minutes >= 43200:
        return 'M'
    elif minutes >= 10080:
        return 'W'
    elif minutes >= 1440:
        return 'D'
    elif minutes >= 60:
        return f'{minutes//60}H'
    elif minutes > 0:
        return f'{minutes}M'
    return 'T'

def _get_timeframe_multiplier(self, minutes):
    """Helper method to get timeframe multiplier"""
    if minutes >= 43200:
        return minutes // 43200
    elif minutes >= 10080:
        return minutes // 10080
    elif minutes >= 1440:
        return minutes // 1440
    elif minutes >= 60:
        return minutes // 60
    return minutes or 1



#builttin function

def _evaluate_builtin_function(self, node):
        args = [self._evaluate(arg) for arg in node['arguments']]

    # Alert and Notification Functions
        if node['name'] == 'alertFunc':
            print(f"ALERT: {args[0]}")
            return None
        elif node['name'] == 'alertConditionFunc':
            return args[0] and args[1]
        elif node['name'] == 'logErrorFunc':
            print(f"ERROR: {args[0]}")
            return None
        elif node['name'] == 'logInfoFunc':
            print(f"INFO: {args[0]}")
            return None
        elif node['name'] == 'logWarningFunc':
            print(f"WARNING: {args[0]}")
            return None

        # Array Functions
        elif node['name'] in ['arrAbs', 'arrAvg', 'arrBinarySearch', 'arrBinarySearchLeftmost', 'arrBinarySearchRightmost', 'arrClear', 'arrConcat', 'arrCopy', 'arrCovariance', 'arrEvery', 'arrFill', 'arrFirst', 'arrFrom', 'arrGet', 'arrIncludes', 'arrIndexOf', 'arrInsert', 'arrJoin', 'arrLast', 'arrLastIndexOf', 'arrMax', 'arrMedian', 'arrMin', 'arrMode', 'arrNewBool', 'arrNewBox', 'arrNewCol', 'arrNewFloat', 'arrNewInt', 'arrNewLabel', 'arrNewLine', 'arrNewLineFill', 'arrNewString', 'arrNewTable', 'arrNewType', 'arrPercentileLinearInterpolation', 'arrPercentileNearestRank', 'arrPercentRank', 'arrPop', 'arrPush', 'arrRange', 'arrRemove', 'arrReverse', 'arrSet', 'arrShift', 'arrSize', 'arrSlice', 'arrSome', 'arrSort', 'arrSortIndices', 'arrStandardize', 'arrStdev', 'arrSum', 'arrUnshift', 'arrVariance']:
            return self._handle_array_operation(node['name'], args)

        # Box Functions
        elif node['name'] in ['boxFunc', 'boxCopyFunc', 'boxDeleteFunc', 'boxGetBottomFunc', 'boxGetLeftFunc', 'boxGetRightFunc', 'boxGetTopFunc', 'boxNewFunc', 'boxSetBgColFunc', 'boxSetBorderColFunc', 'boxSetBorderStyleFunc', 'boxSetBorderWidthFunc', 'boxSetBottomFunc', 'boxSetBottomRightPointFunc', 'boxSetExtendFunc', 'boxSetLeftFunc', 'boxSetLeftTopFunc', 'boxSetRightFunc', 'boxSetRightBottomFunc', 'boxSetTextFunc', 'boxSetTextColFunc', 'boxSetTextFontFamilyFunc', 'boxSetTextHAlignFunc', 'boxSetTextSizeFunc', 'boxSetTextVAlignFunc', 'boxSetTextWrapFunc', 'boxSetTopFunc', 'boxSetTopLeftPointFunc']:
            return self._handle_box_operation(node['name'], args)

        # Chart Functions
        elif node['name'] in ['chartPointCopyFunc', 'chartPointFromIndexFunc', 'chartPointFromTimeFunc',
                             'chartPointNewFunc', 'chartPointNowFunc']:
            return self._handle_chart_operation(node['name'], args)

        # Weird Functions
        elif node['name'] in ['dayOfMonthFunc', 'dayOfWeekFunc', 'fillFunc','fixNanFunc', 'floatFunc','hLineFunc', 'hourFunc', 'indicatorFunc','maxBarsBackFunc', 'minuteFunc', 'monthFunc', 'naFunc','nzFunc', 'polylineDeleteFunc','polylineNewFunc', 'requestCurrencyRateFunc', 'requestDividendsFunc','requestEarningsFunc','requestEconomicFunc', 'requestFinancialFunc', 'requestQuandlFunc', 'requestSecurityFunc','requestSecurityLowerTfFunc', 'requestSeedFunc', 'requestSplitsFunc', 'runtimeErrorFunc','secondFunc','barColFunc','bgColFunc', 'boolFunc']:
            return self._handle_weird_operation(node['name'], args)

        # Color Functions
        elif node['name'] in ['colFunc', 'colBFunc', 'colFromGradientFunc', 'colGFunc', 'colNewFunc','colRFunc', 'colRgbFunc', 'colTFunc']:
            return self._handle_color_operation(node['name'], args)

        # Input Functions
        elif node['name'] in ['inputFunc','inputBoolFunc', 'inputColFunc', 'inputEnumFunc', 'inputFloatFunc','inputIntFunc','inputPriceFunc', 'inputSessionFunc', 'inputSourceFunc', 'inputStringFunc','inputSymbolFunc','inputTextAreaFunc', 'inputTimeFunc', 'inputTimeFrameFunc', 'intFunc']:
            return self._handle_input_operation(node['name'], args)

        # Label Functions
        elif node['name'] in ['labelFunc','labelCopyFunc', 'labelDeleteFunc', 'labelGetTextFunc', 'labelGetXFunc', 'labelGetYFunc','labelNewFunc', 'labelSetColFunc', 'labelSetPointFunc', 'labelSetSizeFunc', 'labelSetStyleFunc','labelSetTextFunc', 'labelSetTextFontFamilyFunc', 'labelSetTextAlignFunc', 'labelSetTextColFunc','labelSetToolTipFunc', 'labelSetXFunc', 'labelSetXLocFunc', 'labelSetXYFunc', 'labelSetYFunc','labelSetYLocFunc']:
            return self._handle_label_operation(node['name'], args)

        # Line Functions
        elif node['name'] in ['libraryFunc', 'lineFunc', 'lineCopyFunc', 'lineDeleteFunc','lineGetPriceFunc', 'lineGetX1Func','lineGetX2Func', 'lineGetY1Func', 'lineGetY2Func','lineNewFunc', 'lineSetColFunc', 'lineSetExtendFunc','lineSetFirstPointFunc','lineSetSecondPointFunc', 'lineSetStyleFunc', 'lineSetWidthFunc', 'lineSetX1Func','lineSetX2Func', 'lineSetXLocFunc', 'lineSetXY1Func', 'lineSetXY2Func', 'lineSetY1Func','lineSetY2Func', 'lineFillFunc', 'lineFillDeleteFunc', 'lineFillGetLine1Func','lineFillGetLine2Func', 'lineFillNewFunc', 'lineFillSetColFunc']:
            return self._handle_line_operation(node['name'], args)

        # log Functions
        elif node['name'] in ['logErrorFunc','logInfoFunc', 'logWarningFunc']:
            return self._handle_log_operation(node['name'], args)

        # map Functions
        elif node['name'] in ['mapClearFunc', 'mapContainsFunc', 'mapCopyFunc','mapGetFunc', 'mapKeysFunc', 'mapNewTypeFunc','mapPutFunc', 'mapPutAllFunc','mapRemoveFunc', 'mapSizeFunc', 'mapValuesFunc']:
            return self._handle_map_operation(node['name'], args)

        # Math Functions
        elif node['name'] in ['mathAbsFunc', 'mathAcosFunc','mathAsinFunc', 'mathAtanFunc', 'mathAvgFunc', 'mathCeilFunc','mathCosFunc','mathExpFunc', 'mathFloorFunc', 'mathLogFunc', 'mathLog10Func', 'mathMaxFunc','mathMinFunc', 'mathPowFunc', 'mathRandomFunc', 'mathRoundFunc', 'mathRoundToMinTickFunc','mathSignFunc', 'mathSinFunc', 'mathSqrtFunc', 'mathSumFunc', 'mathTanFunc','mathToDegreesFunc', 'mathToRadiansFunc']:
            return self._handle_math_operation(node['name'], args)

        # Matrix Functions
        elif node['name'] in ['matrixAddColFunc', 'matrixAddRowFunc','matrixAvgFunc', 'matrixColFunc', 'matrixColumnsFunc', 'matrixConcatFunc', 'matrixCopyFunc','matrixDetFunc', 'matrixDiffFunc', 'matrixEigenValuesFunc', 'matrixEigenVectorsFunc','matrixElementsCountFunc', 'matrixFillFunc', 'matrixGetFunc', 'matrixInvFunc','matrixIsAntiDiagonalFunc', 'matrixIsAntiSymmetricFunc', 'matrixIsBinaryFunc','matrixIsDiagonalFunc','matrixIsIdentityFunc', 'matrixIsSquareFunc', 'matrixIsStochasticFunc','matrixIsSymmetricFunc','matrixIsTriangularFunc', 'matrixIsZeroFunc', 'matrixKronFunc','matrixMaxFunc', 'matrixMedianFunc','matrixMinFunc', 'matrixModeFunc', 'matrixMultFunc','matrixNewTypeFunc', 'matrixPinvFunc', 'matrixPowFunc','matrixRankFunc', 'matrixRemoveColFunc','matrixRemoveRowFunc', 'matrixReshapeFunc', 'matrixReverseFunc','matrixRowFunc','matrixRowsFunc', 'matrixSetFunc', 'matrixSortFunc', 'matrixSubMatrixFunc', 'matrixSumFunc','matrixSwapColumnsFunc', 'matrixSwapRowsFunc', 'matrixTraceFunc', 'matrixTransposeFunc']:
            return self._handle_matrix_operation(node['name'], args)

        # str Functions
        elif node['name'] in ['strContainsFunc', 'strEndsWithFunc', 'strFormatFunc', 'strFormatTimeFunc','strLengthFunc', 'strLowerFunc', 'strMatchFunc', 'strPosFunc', 'strRepeatFunc','strReplaceFunc', 'strReplaceAllFunc', 'strSplitFunc', 'strStartsWithFunc', 'strSubstringFunc','strToNumberFunc', 'strToStringFunc', 'strTrimFunc', 'strUpperFunc']:
            return self._handle_str_operation(node['name'], args)

        # ta Functions
        elif node['name'] in ['taAlmaFunc', 'taAtrFunc', 'taBarsSinceFunc', 'taBbFunc', 'taBbwFunc', 'taCciFunc', 'taChangeFunc', 'taCmoFunc', 'taCogFunc', 'taCorrelationFunc', 'taCrossFunc', 'taCrossoverFunc', 'taCrossunderFunc', 'taCumFunc', 'taDevFunc', 'taDmiFunc', 'taEmaFunc', 'taFallingFunc', 'taHighestFunc', 'taHighestBarsFunc', 'taHmaFunc', 'taKcFunc', 'taKcwFunc', 'taLinRegFunc', 'taLowestFunc', 'taLowestBarsFunc', 'taMacdFunc', 'taMaxFunc', 'taMedianFunc', 'taMfiFunc', 'taMinFunc', 'taModeFunc', 'taMomFunc', 'taPercentileLinearInterpolationFunc', 'taPercentileNearestRankFunc', 'taPercentRankFunc', 'taPivotPointLevelsFunc', 'taPivotHighFunc', 'taPivotLowFunc', 'taRangeFunc', 'taRisingFunc', 'taRmaFunc', 'taRocFunc', 'taRsiFunc', 'taSarFunc', 'taSmaFunc', 'taStdevFunc', 'taStochFunc', 'taSuperTrendFunc', 'taSwmaFunc', 'taTrFunc', 'taTsiFunc', 'taValueWhenFunc', 'taVarianceFunc', 'taVwapFunc', 'taVwmaFunc', 'taWmaFunc', 'taWprFunc']:
            return self._handle_ta_operation(node['name'], args)

        # table Functions
        elif node['name'] in ['tableFunc', 'tableCellFunc', 'tableCellSetBgColFunc', 'tableCellSetHeightFunc', 'tableCellSetTextFunc', 'tableCellSetTextColFunc', 'tableCellSetTextFontFamilyFunc', 'tableCellSetTextHAlignFunc', 'tableCellSetTextSizeFunc', 'tableCellSetTextVAlignFunc', 'tableCellSetToolTipFunc', 'tableCellSetWidthFunc', 'tableClearFunc', 'tableDeleteFunc', 'tableMergeCellsFunc', 'tableNewFunc', 'tableSetBgColFunc', 'tableSetBorderColFunc', 'tableSetBorderWidthFunc', 'tableSetFrameColFunc', 'tableSetFrameWidthFunc', 'tableSetPositionFunc']:
            return self._handle_table_operation(node['name'], args)


        # ticker Functions
        elif node['name'] in [ 'tickerHeikinAshiFunc', 'tickerInheritFunc', 'tickerKagiFunc', 'tickerLineBreakFunc', 'tickerModifyFunc', 'tickerNewFunc', 'tickerPointFigureFunc', 'tickerRenkoFunc', 'tickerStandardFunc']:
            return self._handle_ticker_operation(node['name'], args)
        

        # utility Functions
        elif node['name'] in ['fillFunc', 'fixNanFunc', 'floatFunc', 'hLineFunc', 'indicatorFunc', 'intFunc', 'libraryFunc', 'maxBarsBackFunc', 'naFunc', 'nzFunc', 'polylineDeleteFunc', 'polylineNewFunc', 'runtimeErrorFunc', 'stringFunc', 'symInfoPrefixFunc', 'symInfoTickerFunc']:
            return self._handle_utility_operation(node['name'], args)



        # Strategy Functions
        elif node['name'] in ['strategyFunc','strategyCancelFunc', 'strategyCancelAllFunc', 'strategyCloseFunc', 'strategyCloseAllFunc','strategyClosedTradesCommissionFunc', 'strategyClosedTradesEntryBarIndexFunc','strategyClosedTradesEntryCommentFunc', 'strategyClosedTradesEntryIdFunc','strategyClosedTradesEntryPriceFunc','strategyClosedTradesEntryTimeFunc','strategyClosedTradesExitBarIndexFunc', 'strategyClosedTradesExitCommentFunc','strategyClosedTradesExitIdFunc', 'strategyClosedTradesExitPriceFunc','strategyClosedTradesExitTimeFunc','strategyClosedTradesMaxDrawdownFunc','strategyClosedTradesMaxDrawdownPercentFunc', 'strategyClosedTradesMaxRunupFunc','strategyClosedTradesMaxRunupPercentFunc', 'strategyClosedTradesProfitFunc','strategyClosedTradesProfitPercentFunc','strategyClosedTradesSizeFunc','strategyConver,ToAccountFunc', 'strategyConvertToSymbolFunc', 'strategyDefaultEntryQtyFunc','strategyEntryFunc', 'strategyExitFunc', 'strategyOpenTradesCommissionFunc','strategyOpenTradesEntryBarIndexFunc','strategyOpenTradesEntryCommentFunc','strategyOpenTradesEntryIdFunc', 'strategyOpenTradesEntryPriceFunc','strategyOpenTradesEntryTimeFunc', 'strategyOpenTradesMaxDrawdownFunc','strategyOpenTradesMaxDrawdownPercentFunc','strategyOpenTradesMaxRunupFunc','strategyOpenTradesMaxRunupPercentFunc', 'strategyOpenTradesProfitFunc','strategyOpenTradesProfitPercentFunc', 'strategyOpenTradesSizeFunc', 'strategyOrderFunc','strategyRiskAllowEntryInFunc','strategyRiskMaxConsLossDaysFunc', 'strategyRiskMaxDrawdownFunc','strategyRiskMaxIntradayFilledOrdersFunc','strategyRiskMaxIntradayLossFunc','strategyRiskMaxPositionSizeFunc']:
            return self._handle_strategy_operation(node['name'], args)

        # Time Functions
        elif node['name'] in ['symInfoPrefixFunc', 'symInfoTickerFunc', 'timeFunc','timeCloseFunc', 'timeframeChangeFunc','timeframeFromSecondsFunc', 'timeframeInSecondsFunc','timestampFunc', 'weekOfYearFunc', 'yearFunc']:
            return self._handle_time_operation(node['name'], args)

        # Original functions remain unchanged
        elif node['name'] == 'sma':
            return sum(args[0][-args[1]:]) / args[1]
        elif node['name'] == 'ema':
            k = 2 / (args[1] + 1)
            ema = args[0][0]
            for price in args[0][1:]:
                ema = price * k + ema * (1 - k)
            return ema
        elif node['name'] == 'rsi':
            gains = [args[0][i] - args[0][i - 1] for i in range(1, len(args[0])) if args[0][i] > args[0][i - 1]]
            losses = [-args[0][i] + args[0][i - 1] for i in range(1, len(args[0])) if args[0][i] < args[0][i - 1]]
            avg_gain = sum(gains) / args[1]
            avg_loss = sum(losses) / args[1]
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            return 100 - (100 / (1 + rs))

        return None


def _calculate_strategy_metrics(self):
    """Calculates all strategy performance metrics"""
    trades = self.trades  # Assuming we have a trades list
    
    if trades:
        profits = [t['profit'] for t in trades if t['profit'] > 0]
        losses = [t['profit'] for t in trades if t['profit'] < 0]
        
        self.environment.update({
            'strategyAvgTrade': sum(t['profit'] for t in trades) / len(trades),
            'strategyAvgWinningTrade': sum(profits) / len(profits) if profits else 0,
            'strategyAvgLosingTrade': sum(losses) / len(losses) if losses else 0,
            'strategyNetProfit': sum(t['profit'] for t in trades),
            'strategyWinTrades': len(profits),
            'strategyLossTrades': len(losses)
        })

def _calculate_price_aggregates(self):
    """Calculates price aggregates"""
    if self.market_data['high']:
        high = self.market_data['high'][-1]
        low = self.market_data['low'][-1]
        close = self.market_data['close'][-1]
        open_price = self.market_data['open'][-1]
        
        self.environment.update({
            'hl2': (high + low) / 2,
            'hlc3': (high + low + close) / 3,
            'hlcc4': (high + low + 2 * close) / 4,
            'ohlc4': (open_price + high + low + close) / 4
        })

def _calculate_session_states(self):
    """Determines session states based on current time"""
    current_hour = self.current_time.hour
    current_minute = self.current_time.minute
    
    self.environment.update({
        'sessionIsMarket': 9 <= current_hour < 16,
        'sessionIsPreMarket': 4 <= current_hour < 9,
        'sessionIsPostMarket': 16 <= current_hour < 20,
        'sessionIsFirstBar': current_hour == 9 and current_minute == 30,
        'sessionIsLastBar': current_hour == 16 and current_minute == 0
    })

def _calculate_timeframe_states(self):
    """Sets timeframe states based on current configuration"""
    period_minutes = self.environment['timeframePeriod']
    
    self.environment.update({
        'timeframeIsDaily': period_minutes == 1440,
        'timeframeIsWeekly': period_minutes == 10080,
        'timeframeIsMonthly': period_minutes == 43200,
        'timeframeIsMinutes': period_minutes < 1440,
        'timeframeIsIntraday': period_minutes < 1440,
        'timeframeIsDWM': period_minutes >= 1440
    })

def update_all_calculations(self):
    """Updates all calculated values"""
    self._calculate_technical_indicators()
    self._calculate_strategy_metrics()
    self._calculate_price_aggregates()
    self._calculate_session_states()
    self._calculate_timeframe_states()

def _calculate_market_data(self):
    """Market data calculations"""
    if self.market_data['close']:
        self.environment.update({
            'open': self.market_data['open'][-1],
            'high': self.market_data['high'][-1],
            'low': self.market_data['low'][-1],
            'close': self.market_data['close'][-1],
            'volume': self.market_data['volume'][-1]
        })

def _calculate_bar_states(self):
    """Bar state calculations"""
    current_index = len(self.market_data['close']) - 1
    self.environment.update({
        'barIndex': current_index,
        'barStateIsConfirmed': current_index < len(self.market_data['close']) - 1,
        'barStateIsFirst': current_index == 0,
        'barStateIsLast': current_index == len(self.market_data['close']) - 1,
        'barStateIsNew': self.is_new_bar,
        'barStateIsRealtime': self.is_realtime
    })

def _calculate_time_components(self):
    """Time component calculations"""
    current_time = self.current_time
    self.environment.update({
        'dayOfMonth': current_time.day,
        'dayOfWeek': current_time.weekday() + 1,
        'hour': current_time.hour,
        'minute': current_time.minute,
        'month': current_time.month,
        'second': current_time.second,
        'time': current_time.timestamp(),
        'timeClose': (current_time + timedelta(minutes=1)).timestamp(),
        'timeTradingDay': current_time.replace(hour=0, minute=0, second=0).timestamp(),
        'timeNow': current_time.timestamp(),
        'weekOfYear': current_time.isocalendar()[1],
        'year': current_time.year
    })

def _calculate_price_components(self):
    """Price component calculations"""
    if self.market_data['close']:
        high = self.market_data['high'][-1]
        low = self.market_data['low'][-1]
        close = self.market_data['close'][-1]
        open_price = self.market_data['open'][-1]
        
        self.environment.update({
            'hl2': (high + low) / 2,
            'hlc3': (high + low + close) / 3,
            'hlcc4': (high + low + 2 * close) / 4,
            'ohlc4': (open_price + high + low + close) / 4
        })

def _calculate_technical_indicators(self):
    """Technical indicator calculations"""
    if len(self.market_data['close']) > 1:
        close = np.array(self.market_data['close'])
        volume = np.array(self.market_data['volume'])
        high = np.array(self.market_data['high'])
        low = np.array(self.market_data['low'])

        # Accumulation/Distribution Line
        clv = ((close - low) - (high - close)) / (high - low)
        ad = (clv * volume).cumsum()
        
        # On-Balance Volume
        obv = np.zeros_like(close)
        obv[1:] = np.where(close[1:] > close[:-1], volume[1:], 
                          np.where(close[1:] < close[:-1], -volume[1:], 0)).cumsum()
        
        # True Range
        tr = np.maximum(high - low, 
                       np.maximum(abs(high - np.roll(close, 1)), 
                                abs(low - np.roll(close, 1))))
        
        # VWAP
        vwap = (close * volume).cumsum() / volume.cumsum()
        
        self.environment.update({
            'taAccDist': ad[-1],
            'taOBV': obv[-1],
            'taTR': tr[-1],
            'taVWAP': vwap[-1],
            'taIII': (2 * close[-1] - high[-1] - low[-1]) / (high[-1] - low[-1]) * volume[-1]
        })

def _calculate_strategy_metrics(self):
    """Strategy metrics calculations"""
    if self.trades:
        trades_array = np.array([t['profit'] for t in self.trades])
        winning_trades = trades_array[trades_array > 0]
        losing_trades = trades_array[trades_array < 0]
        
        initial_capital = self.environment['strategyInitialCapital']
        current_equity = initial_capital + trades_array.sum()
        
        self.environment.update({
            'strategyNetProfit': trades_array.sum(),
            'strategyNetProfitPercent': (trades_array.sum() / initial_capital) * 100,
            'strategyAvgTrade': trades_array.mean(),
            'strategyAvgWinningTrade': winning_trades.mean() if len(winning_trades) > 0 else 0,
            'strategyAvgLosingTrade': losing_trades.mean() if len(losing_trades) > 0 else 0,
            'strategyWinTrades': len(winning_trades),
            'strategyLossTrades': len(losing_trades),
            'strategyEquity': current_equity
        })

def _calculate_session_states(self):
    """Session state calculations"""
    current_time = self.current_time
    market_open = current_time.replace(hour=9, minute=30)
    market_close = current_time.replace(hour=16, minute=0)
    pre_market_open = current_time.replace(hour=4, minute=0)
    post_market_close = current_time.replace(hour=20, minute=0)
    
    self.environment.update({
        'sessionIsMarket': market_open <= current_time < market_close,
        'sessionIsPreMarket': pre_market_open <= current_time < market_open,
        'sessionIsPostMarket': market_close <= current_time < post_market_close,
        'sessionIsFirstBar': current_time == market_open,
        'sessionIsLastBar': current_time == market_close
    })

def _calculate_timeframe_states(self):
    """Timeframe state calculations"""
    period_minutes = self.environment['timeframePeriod']
    
    self.environment.update({
        'timeframeIsDaily': period_minutes == 1440,
        'timeframeIsWeekly': period_minutes == 10080,
        'timeframeIsMonthly': period_minutes == 43200,
        'timeframeIsMinutes': period_minutes < 1440,
        'timeframeIsSeconds': period_minutes < 1,
        'timeframeIsTicks': period_minutes == 0,
        'timeframeIsIntraday': period_minutes < 1440,
        'timeframeIsDWM': period_minutes >= 1440,
        'timeframeMainPeriod': self._get_timeframe_period_string(period_minutes),
        'timeframeMultiplier': self._get_timeframe_multiplier(period_minutes)
    })

def _get_timeframe_period_string(self, minutes):
    """Helper method to get timeframe period string"""
    if minutes >= 43200:
        return 'M'
    elif minutes >= 10080:
        return 'W'
    elif minutes >= 1440:
        return 'D'
    elif minutes >= 60:
        return f'{minutes//60}H'
    elif minutes > 0:
        return f'{minutes}M'
    return 'T'

def _get_timeframe_multiplier(self, minutes):
    """Helper method to get timeframe multiplier"""
    if minutes >= 43200:
        return minutes // 43200
    elif minutes >= 10080:
        return minutes // 10080
    elif minutes >= 1440:
        return minutes // 1440
    elif minutes >= 60:
        return minutes // 60
    return minutes or 1





#Constant

def constant(self, name):

    def calc_style(style_type, value):
        return {'type': style_type, 'value': value, 'enabled': True}

    def calc_position(x, y, value):
        return {'x': x, 'y': y, 'value': value, 'active': True}

    def calc_scale(direction, value):
        return {'direction': direction, 'value': value, 'visible': True}

    def calc_session(type, hours):
        return {'type': type, 'hours': hours, 'active': True}

    def calc_shape(shape_type, properties):
        return {'type': shape_type, **properties, 'visible': True}

    def calc_size(type, scale):
        return {'type': type, 'scale': scale, 'active': True}

    def calc_strategy(strat_type, properties):
        return {'type': strat_type, **properties, 'enabled': True}

    def calc_text(align, value):
        return {'align': align, 'value': value, 'visible': True}

    def calc_location(coord_type, value):
        return {'type': coord_type, 'value': value, 'active': True}

    def calc_color(rgb, alpha=1.0):
        return {'rgb': rgb, 'alpha': alpha, 'visible': True}

    def calc_currency(code, decimals):
        return {'code': code, 'decimals': decimals, 'active': True}

    # Main calculation dictionary
    calculations = {
        # Style calculations
        'showStyleArea': lambda: calc_style('area', 1),
        'showStyleAreaBr': lambda: calc_style('area_break', 2),
        'showStyleCircles': lambda: calc_style('circles', 3),
        'showStyleColumns': lambda: calc_style('columns', 4),
        'showStyleCross': lambda: calc_style('cross', 5),
        'showStyleHistogram': lambda: calc_style('histogram', 6),
        'showStyleLine': lambda: calc_style('line', 7),
        'showStyleLineBr': lambda: calc_style('line_break', 8),
        'showStyleStepLine': lambda: calc_style('stepline', 9),
        'showStyleStepLineDiamond': lambda: calc_style('stepline_diamond', 10),
        'showStyleStepLineBr': lambda: calc_style('stepline_break', 11),

        # Position calculations
        'positionBottomCenter': lambda: calc_position(0.5, 1.0, 12),
        'positionBottomLeft': lambda: calc_position(0.0, 1.0, 13),
        'positionBottomRight': lambda: calc_position(1.0, 1.0, 14),
        'positionMiddleCenter': lambda: calc_position(0.5, 0.5, 15),
        'positionMiddleLeft': lambda: calc_position(0.0, 0.5, 16),
        'positionMiddleRight': lambda: calc_position(1.0, 0.5, 17),
        'positionTopCenter': lambda: calc_position(0.5, 0.0, 18),
        'positionTopLeft': lambda: calc_position(0.0, 0.0, 19),
        'positionTopRight': lambda: calc_position(1.0, 0.0, 20),

        # Scale calculations
        'scaleLeft': lambda: calc_scale('left', -1),
        'scaleNone': lambda: calc_scale('none', 0),
        'scaleRight': lambda: calc_scale('right', 1),

        # Session calculations
        'sessionExtended': lambda: calc_session('extended', 24),
        'sessionRegular': lambda: calc_session('regular', 8),
        'settlementAsCloseInherit': lambda: {'type': 'inherit', 'value': True},
        'settlementAsCloseOff': lambda: {'type': 'off', 'value': False},
        'settlementAsCloseOn': lambda: {'type': 'on', 'value': True},

        # Shape calculations
        'shapeArrowDown': lambda: calc_shape('arrow', {'direction': 'down', 'angle': 270}),
        'shapeArrowUp': lambda: calc_shape('arrow', {'direction': 'up', 'angle': 90}),
        'shapeCircle': lambda: calc_shape('circle', {'radius': 1}),
        'shapeCross': lambda: calc_shape('cross', {'size': 1}),
        'shapeDiamond': lambda: calc_shape('diamond', {'size': 1}),
        'shapeFlag': lambda: calc_shape('flag', {'size': 1}),
        'shapeLabelDown': lambda: calc_shape('label', {'direction': 'down'}),
        'shapeLabelUp': lambda: calc_shape('label', {'direction': 'up'}),
        'shapeSquare': lambda: calc_shape('square', {'size': 1}),
        'shapeTriangleDown': lambda: calc_shape('triangle', {'direction': 'down'}),
        'shapeTriangleUp': lambda: calc_shape('triangle', {'direction': 'up'}),
        'shapeXCross': lambda: calc_shape('xcross', {'size': 1}),

        # Size calculations
        'sizeAuto': lambda: calc_size('auto', 1.0),
        'sizeHuge': lambda: calc_size('fixed', 2.0),
        'sizeLarge': lambda: calc_size('fixed', 1.5),
        'sizeNormal': lambda: calc_size('fixed', 1.0),
        'sizeSmall': lambda: calc_size('fixed', 0.75),
        'sizeTiny': lambda: calc_size('fixed', 0.5),

        # Strategy calculations
        'strategyCash': lambda: calc_strategy('cash', {'value': 1000}),
        'strategyCommissionCashPerContract': lambda: calc_strategy('commission', {'method': 'per_contract'}),
        'strategyCommissionCashPerOrder': lambda: calc_strategy('commission', {'method': 'per_order'}),
        'strategyCommissionPercent': lambda: calc_strategy('commission', {'method': 'percent'}),
        'strategyDirectionAll': lambda: calc_strategy('direction', {'value': 'all'}),
        'strategyDirectionLong': lambda: calc_strategy('direction', {'value': 'long'}),
        'strategyDirectionShort': lambda: calc_strategy('direction', {'value': 'short'}),
        'strategyFixed': lambda: calc_strategy('fixed', {'value': True}),
        'strategyLong': lambda: calc_strategy('position', {'value': 'long'}),
        'strategyOcaCancel': lambda: calc_strategy('oca', {'action': 'cancel'}),
        'strategyOcaNone': lambda: calc_strategy('oca', {'action': 'none'}),
        'strategyOcaReduce': lambda: calc_strategy('oca', {'action': 'reduce'}),
        'strategyPercentOfEquity': lambda: calc_strategy('percent_equity', {'value': 100}),
        'strategyShort': lambda: calc_strategy('position', {'value': 'short'}),
        
        # Boolean Constants
        'trueValue': lambda: True,
        'falseValue': lambda: False,

        # Text calculations
        'textAlignBottom': lambda: calc_text('bottom', 'bottom'),
        'textAlignCenter': lambda: calc_text('center', 'center'),
        'textAlignLeft': lambda: calc_text('left', 'left'),
        'textAlignRight': lambda: calc_text('right', 'right'),
        'textAlignTop': lambda: calc_text('top', 'top'),
        'textWrapAuto': lambda: {'wrap': 'auto', 'value': True},
        'textWrapNone': lambda: {'wrap': 'none', 'value': False},

        # Location calculations
        'locationAboveBar': lambda: calc_location('above', {'y': 1, 'offset': 5}),
        'locationAbsolute': lambda: calc_location('absolute', {'value': True}),
        'locationBelowBar': lambda: calc_location('below', {'y': -1, 'offset': -5}),
        'locationBottom': lambda: calc_location('bottom', {'y': -1}),
        'locationTop': lambda: calc_location('top', {'y': 1}),


        # Adjustment Constants
         'adjustmentDividends': lambda: 'dividends',
         'adjustmentNone': lambda: 'none',
         'adjustmentSplits': lambda: 'splits',

        # Alert Constants
          'alertFreqAll': lambda: 'all',
          'alertFreqOncePerBar': lambda: 'once_per_bar',
          'alertFreqOncePerBarClose': lambda: 'once_per_bar_close',

         # Bar Merge Constants
         'barMergeGapsOff': lambda: False,
         'barMergeGapsOn': lambda: True,
         'barMergeLookaheadOff': lambda: False,
         'barMergeLookaheadOn': lambda: True,


        # Math calculations
        'mathE': lambda: 2.718281828459045,
        'mathPi': lambda: 3.141592653589793,
        'mathPhi': lambda: 1.618033988749895,
        'mathRPhi': lambda: 0.618033988749895,

        # Color calculations
        'colAqua': lambda: calc_color('#00FFFF'),
        'colBlack': lambda: calc_color('#000000'),
        'colBlue': lambda: calc_color('#0000FF'),
        'colFuchsia': lambda: calc_color('#FF00FF'),
        'colGray': lambda: calc_color('#808080'),
        'colGreen': lambda: calc_color('#008000'),
        'colLime': lambda: calc_color('#00FF00'),
        'colMaroon': lambda: calc_color('#800000'),
        'colNavy': lambda: calc_color('#000080'),
        'colOlive': lambda: calc_color('#808000'),
        'colOrange': lambda: calc_color('#FFA500'),
        'colPurple': lambda: calc_color('#800080'),
        'colRed': lambda: calc_color('#FF0000'),
        'colSilver': lambda: calc_color('#C0C0C0'),
        'colTeal': lambda: calc_color('#008080'),
        'colWhite': lambda: calc_color('#FFFFFF'),
        'colYellow': lambda: calc_color('#FFFF00'),

        # Currency calculations
        'currencyAUD': lambda: calc_currency('AUD', 2),
        'currencyBTC': lambda: calc_currency('BTC', 8),
        'currencyCAD': lambda: calc_currency('CAD', 2),
        'currencyCHF': lambda: calc_currency('CHF', 2),
        'currencyETH': lambda: calc_currency('ETH', 8),
        'currencyEUR': lambda: calc_currency('EUR', 2),
        'currencyGBP': lambda: calc_currency('GBP', 2),
        'currencyHKD': lambda: calc_currency('HKD', 2),
        'currencyINR': lambda: calc_currency('INR', 2),
        'currencyJPY': lambda: calc_currency('JPY', 0),
        'currencyKRW': lambda: calc_currency('KRW', 0),
        'currencyMYR': lambda: calc_currency('MYR', 2),
        'currencyNOK': lambda: calc_currency('NOK', 2),
        'currencyNZD': lambda: calc_currency('NZD', 2),
        'currencyRUB': lambda: calc_currency('RUB', 2),
        'currencySEK': lambda: calc_currency('SEK', 2),
        'currencySGD': lambda: calc_currency('SGD', 2),
        'currencyTRY': lambda: calc_currency('TRY', 2),
        'currencyUSD': lambda: calc_currency('USD', 2),
        'currencyUSDT': lambda: calc_currency('USDT', 2),
        'currencyZAR': lambda: calc_currency('ZAR', 2),

        # Boolean calculations
        'trueValue': lambda: True,
        'falseValue': lambda: False,

        # Day calculations
        'dayOfWeekSunday': lambda: 0,
        'dayOfWeekMonday': lambda: 1,
        'dayOfWeekTuesday': lambda: 2,
        'dayOfWeekWednesday': lambda: 3,
        'dayOfWeekThursday': lambda: 4,
        'dayOfWeekFriday': lambda: 5,
        'dayOfWeekSaturday': lambda: 6
    }

    return calculations.get(name, lambda: None)()







#Type_Declaration

def _handle_type_declaration(self, node, args):
    # Create type registry if it doesn't exist
    if not hasattr(self, '_type_registry'):
        self._type_registry = {}
    
    # Handle different type declarations
    if node == 'arr':
        return {'type': 'array', 'value': args[0] if args else []}
    
    elif node == 'bool':
        return {'type': 'boolean', 'value': bool(args[0]) if args else False}
    
    elif node == 'box':
        return {'type': 'box', 'properties': {
            'left': args[0] if len(args) > 0 else 0,
            'top': args[1] if len(args) > 1 else 0,
            'right': args[2] if len(args) > 2 else 0,
            'bottom': args[3] if len(args) > 3 else 0
        }}
    
    elif node == 'chartPoint':
        return {'type': 'chartPoint', 'coordinates': {
            'x': args[0] if len(args) > 0 else 0,
            'y': args[1] if len(args) > 1 else 0
        }}
    
    elif node == 'col':
        r = args[0] if len(args) > 0 else 0
        g = args[1] if len(args) > 1 else 0
        b = args[2] if len(args) > 2 else 0
        a = args[3] if len(args) > 3 else 255
        return {'type': 'color', 'rgba': (r, g, b, a)}
    
    elif node == 'const':
        return {'type': 'constant', 'value': args[0], 'mutable': False}
    
    elif node == 'float':
        return {'type': 'float', 'value': float(args[0]) if args else 0.0}
    
    elif node == 'int':
        return {'type': 'integer', 'value': int(args[0]) if args else 0}
    
    elif node == 'label':
        return {'type': 'label', 'properties': {
            'text': args[0] if len(args) > 0 else '',
            'position': {'x': args[1] if len(args) > 1 else 0, 
                        'y': args[2] if len(args) > 2 else 0}
        }}
    
    elif node == 'line':
        return {'type': 'line', 'points': {
            'start': {'x': args[0] if len(args) > 0 else 0, 
                     'y': args[1] if len(args) > 1 else 0},
            'end': {'x': args[2] if len(args) > 2 else 0, 
                   'y': args[3] if len(args) > 3 else 0}
        }}
    
    elif node == 'lineFill':
        return {'type': 'lineFill', 'properties': {
            'line1': args[0] if len(args) > 0 else None,
            'line2': args[1] if len(args) > 1 else None,
            'color': args[2] if len(args) > 2 else None
        }}
    
    elif node == 'map':
        return {'type': 'map', 'value': dict(zip(args[::2], args[1::2])) if args else {}}
    
    elif node == 'matrx':
        rows = args[0] if len(args) > 0 else 0
        cols = args[1] if len(args) > 1 else 0
        default_value = args[2] if len(args) > 2 else 0
        matrix = [[default_value for _ in range(cols)] for _ in range(rows)]
        return {'type': 'matrix', 'value': matrix, 'dimensions': (rows, cols)}
    
    elif node == 'polyline':
        return {'type': 'polyline', 'points': args[0] if args else []}
    
    elif node == 'series':
        return {'type': 'series', 'values': args[0] if args else [], 'timeframe': args[1] if len(args) > 1 else None}
    
    elif node == 'simple':
        return {'type': 'simple', 'value': args[0] if args else None}
    
    elif node == 'string':
        return {'type': 'string', 'value': str(args[0]) if args else ''}
    
    elif node == 'table':
        return {'type': 'table', 'rows': args[0] if len(args) > 0 else [],
                'headers': args[1] if len(args) > 1 else []}

    self._type_registry[node] = {'type': node, 'args': args}
    
    return self._type_registry[node]






#environment
class Environment:
    def __init__(self):
        self.market_data = {
            'open': [],
            'high': [],
            'low': [],
            'close': [],
            'volume': []
        }
        
        self.current_time = datetime.now()
        
        self.environment = {
            # Market Data - Updated with each tick/bar
            'open': self.market_data['open'][-1] if self.market_data['open'] else 0,
            'high': self.market_data['high'][-1] if self.market_data['high'] else 0,
            'low': self.market_data['low'][-1] if self.market_data['low'] else 0,
            'close': self.market_data['close'][-1] if self.market_data['close'] else 0,
            'volume': self.market_data['volume'][-1] if self.market_data['volume'] else 0,
            
            # Bar State
            'barIndex': len(self.market_data['close']) - 1 if self.market_data['close'] else 0,
            'barStateIsConfirmed': True,  # Updated based on real-time data
            'barStateIsFirst': len(self.market_data['close']) == 1,
            'barStateIsHistory': True,  # Updated based on real-time data
            'barStateIsLast': True,  # Updated with each new bar
            'barStateIsLastConfirmedHistory': True,  # Updated with real-time data
            'barStateIsNew': False,  # Updated with each new bar
            'barStateIsRealtime': False,  # Updated with real-time data
            
            # Chart Elements
            'boxAll': [],  # List of all box objects
            'chartBgCol': '#FFFFFF',  # Default white background
            'chartFgCol': '#000000',  # Default black foreground
            'chartIsHeikinAshi': False,
            'chartIsKagi': False,
            'chartIsLineBreak': False,
            'chartIsPnf': False,
            'chartIsRange': False,
            'chartIsRenko': False,
            'chartIsStandard': True,
            'chartLeftVisibleBarTime': self.current_time - timedelta(days=100),
            'chartRightVisibleBarTime': self.current_time,
            
            # Time Components
            'dayOfMonth': self.current_time.day,
            'dayOfWeek': self.current_time.weekday() + 1,
            'hour': self.current_time.hour,
            'minute': self.current_time.minute,
            'month': self.current_time.month,
            'second': self.current_time.second,
            'time': self.current_time.timestamp(),
            'timeClose': (self.current_time + timedelta(minutes=1)).timestamp(),
            'timeTradingDay': self.current_time.replace(hour=0, minute=0, second=0).timestamp(),
            'timeNow': self.current_time.timestamp(),
            'weekOfYear': self.current_time.isocalendar()[1],
            'year': self.current_time.year,
            
            # Price Calculations
            'hl2': (self.market_data['high'][-1] + self.market_data['low'][-1]) / 2 if self.market_data['high'] else 0,
            'hlc3': (self.market_data['high'][-1] + self.market_data['low'][-1] + self.market_data['close'][-1]) / 3 if self.market_data['high'] else 0,
            'hlcc4': (self.market_data['high'][-1] + self.market_data['low'][-1] + 2 * self.market_data['close'][-1]) / 4 if self.market_data['high'] else 0,
            'ohlc4': (self.market_data['open'][-1] + self.market_data['high'][-1] + self.market_data['low'][-1] + self.market_data['close'][-1]) / 4 if self.market_data['high'] else 0,
            
            # UI Elements
            'labelAll': [],
            'lastBarIndex': len(self.market_data['close']) - 1 if self.market_data['close'] else 0,
            'lastBarTime': self.current_time.timestamp(),
            'lineAll': [],
            'lineFillAll': [],
            'polylineAll': [],
            'tableAll': [],
            
            # Special Values
            'na': None,
            
            # Session States (example implementation - should be updated based on actual market hours)
            'sessionIsFirstBar': False,
            'sessionIsFirstBarRegular': False,
            'sessionIsLastBar': False,
            'sessionIsLastBarRegular': False,
            'sessionIsMarket': 9 <= self.current_time.hour < 16,  # Example: 9:00-16:00 market hours
            'sessionIsPostMarket': 16 <= self.current_time.hour < 20,  # Example: 16:00-20:00 post-market
            'sessionIsPreMarket': 4 <= self.current_time.hour < 9,  # Example: 4:00-9:00 pre-market
            
            # Strategy Metrics (initialized with default values)
            'strategyAccountCurrency': 'USD',
            'strategyAvgLosingTrade': 0,
            'strategyAvgLosingTradePercent': 0,
            'strategyAvgTrade': 0,
            'strategyAvgTradePercent': 0,
            'strategyAvgWinningTrade': 0,
            'strategyAvgWinningTradePercent': 0,
            'strategyClosedTrades': 0,
            'strategyClosedTradesFirstIndex': 0,
            'strategyEquity': 10000,  # Example initial equity
            'strategyEvenTrades': 0,
            'strategyGrossLoss': 0,
            'strategyGrossLossPercent': 0,
            'strategyGrossProfit': 0,
            'strategyGrossProfitPercent': 0,
            'strategyInitialCapital': 10000,
            'strategyLossTrades': 0,
            'strategyMarginLiquidationPrice': 0,
            'strategyMaxContractsHeldAll': 0,
            'strategyMaxContractsHeldLong': 0,
            'strategyMaxContractsHeldShort': 0,
            'strategyMaxDrawdown': 0,
            'strategyMaxDrawdownPercent': 0,
            'strategyMaxRunup': 0,
            'strategyMaxRunupPercent': 0,
            'strategyNetProfit': 0,
            'strategyNetProfitPercent': 0,
            'strategyOpenProfit': 0,
            'strategyOpenProfitPercent': 0,
            'strategyOpenTrades': 0,
            'strategyOpenTradesCapitalHeld': 0,
            'strategyPositionAvgPrice': 0,
            'strategyPositionEntryName': '',
            'strategyPositionSize': 0,
            'strategyWinTrades': 0,
            
            # Symbol Information (example values)
            'symInfoBaseCurrency': 'USD',
            'symInfoCountry': 'US',
            'symInfoCurrency': 'USD',
            'symInfoDescription': 'Example Stock',
            'symInfoEmployees': 1000,
            'symInfoExpirationDate': None,
            'symInfoIndustry': 'Technology',
            'symInfoMainTickerId': 'EXAMPLE',
            'symInfoMinContract': 1,
            'symInfoMinMove': 0.01,
            'symInfoMinTick': 0.01,
            'symInfoPointValue': 1.0,
            'symInfoPrefix': '',
            'symInfoPriceScale': 2,
            'symInfoRecommendationsBuy': 0,
            'symInfoRecommendationsBuyStrong': 0,
            'symInfoRecommendationsDate': self.current_time.timestamp(),
            'symInfoRecommendationsHold': 0,
            'symInfoRecommendationsSell': 0,
            'symInfoRecommendationsSellStrong': 0,
            'symInfoRecommendationsTotal': 0,
            'symInfoRoot': 'EXAMPLE',
            'symInfoSector': 'Technology',
            'symInfoSession': 'Regular',
            'symInfoShareholders': 10000,
            'symInfoSharesOutstandingFloat': 1000000,
            'symInfoSharesOutstandingTotal': 1200000,
            'symInfoTargetPriceAverage': 0,
            'symInfoTargetPriceDate': self.current_time.timestamp(),
            'symInfoTargetPriceEstimates': 0,
            'symInfoTargetPriceHigh': 0,
            'symInfoTargetPriceLow': 0,
            'symInfoTargetPriceMedian': 0,
            'symInfoTicker': 'EXAMPLE',
            'symInfoTickerId': 'EXAMPLE',
            'symInfoTimezone': 'America/New_York',
            'symInfoType': 'Stock',
            'symInfoVolumeType': 'Base',
            
            # Technical Analysis (initialized with default values)
            'taAccDist': 0,
            'taIII': 0,
            'taNVI': 0,
            'taOBV': 0,
            'taPVI': 0,
            'taPVT': 0,
            'taTR': 0,
            'taVWAP': 0,
            'taWAD': 0,
            'taWVAD': 0,
            
            # Timeframe Information
            'timeframeIsDaily': True,
            'timeframeIsDWM': True,
            'timeframeIsIntraday': False,
            'timeframeIsMinutes': False,
            'timeframeIsMonthly': False,
            'timeframeIsSeconds': False,
            'timeframeIsTicks': False,
            'timeframeIsWeekly': False,
            'timeframeMainPeriod': 'D',
            'timeframeMultiplier': 1,
            'timeframePeriod': 1440  # Minutes in a day
        }

    def update_market_data(self, open_price, high_price, low_price, close_price, volume):
        """Updates market data and recalculates dependent variables"""
        self.market_data['open'].append(open_price)
        self.market_data['high'].append(high_price)
        self.market_data['low'].append(low_price)
        self.market_data['close'].append(close_price)
        self.market_data['volume'].append(volume)
        self._update_calculated_values()

    def _update_calculated_values(self):
        """Updates all calculated values based on new market data"""
        self.environment.update({
            'open': self.market_data['open'][-1],
            'high': self.market_data['high'][-1],
            'low': self.market_data['low'][-1],
            'close': self.market_data['close'][-1],
            'volume': self.market_data['volume'][-1],
            'barIndex': len(self.market_data['close']) - 1,
            'hl2': (self.market_data['high'][-1] + self.market_data['low'][-1]) / 2,
            'hlc3': (self.market_data['high'][-1] + self.market_data['low'][-1] + self.market_data['close'][-1]) / 3,
            'hlcc4': (self.market_data['high'][-1] + self.market_data['low'][-1] + 2 * self.market_data['close'][-1]) / 4,
            'ohlc4': (self.market_data['open'][-1] + self.market_data['high'][-1] + self.market_data['low'][-1] + self.market_data['close'][-1]) / 4,
        })

    def get(self, key, default=None):
        """Gets a value from the environment"""
        return self.environment.get(key, default)

    def set(self, key, value):
        """Sets a value in the environment"""
        self.environment[key] = value







#Keyword
def _handle_keyword_operation(self, operation, args):
    # Control Flow Operations
    if operation == 'ifCond':
        condition = args[0]
        if condition:
            return self._evaluate(args[1])  # True block
        elif len(args) > 2:
            return self._evaluate(args[2])  # Else block
        return None

    elif operation == 'forLoop':
        init, condition, increment, body = args
        self._evaluate(init)
        while self._evaluate(condition):
            result = self._evaluate(body)
            self._evaluate(increment)
        return result

    elif operation == 'forInLoop':
        iterator, collection, body = args
        for item in self._evaluate(collection):
            self.variables[iterator] = item
            result = self._evaluate(body)
        return result

    elif operation == 'whileLoop':
        condition, body = args
        while self._evaluate(condition):
            result = self._evaluate(body)
        return result

    elif operation == 'switchCase':
        value, cases, default = args
        for case in cases:
            if self._evaluate(case['condition']) == value:
                return self._evaluate(case['body'])
        return self._evaluate(default) if default else None

    # Logical Operations
    elif operation == 'andOp':
        return bool(self._evaluate(args[0]) and self._evaluate(args[1]))

    elif operation == 'orOp':
        return bool(self._evaluate(args[0]) or self._evaluate(args[1]))

    elif operation == 'notOp':
        return not bool(self._evaluate(args[0]))

    # Variable Declaration Operations
    elif operation == 'let':
        name, value = args
        self.variables[name] = self._evaluate(value)
        return self.variables[name]

    elif operation == 'letip':
        name, default_value, options = args
        value = self._get_input_value(name, default_value, options)
        self.variables[name] = value
        return value

    # Type System Operations
    elif operation == 'typeDef':
        name, properties = args
        self.types[name] = properties
        return self.types[name]

    elif operation == 'enumType':
        name, values = args
        enum_dict = {val: idx for idx, val in enumerate(values)}
        self.enums[name] = enum_dict
        return enum_dict

    # Module System Operations
    elif operation == 'importFunc':
        module_name = args[0]
        imported_module = self._import_module(module_name)
        return imported_module

    elif operation == 'exportFunc':
        export_items = args[0]
        return self._export_items(export_items)

    elif operation == 'methodFunc':
        name, params, body = args
        self.functions[name] = {
            'params': params,
            'body': body
        }
        return self.functions[name]

    return None



#Array
def _handle_array_operation(self, operation_name, args):
    if operation_name == 'arrAbs':
        return [abs(x) for x in args[0]]
    
    elif operation_name == 'arrAvg':
        return sum(args[0]) / len(args[0]) if args[0] else 0
    
    elif operation_name == 'arrBinarySearch':
        target = args[1]
        left, right = 0, len(args[0]) - 1
        while left <= right:
            mid = (left + right) // 2
            if args[0][mid] == target:
                return mid
            elif args[0][mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    elif operation_name == 'arrBinarySearchLeftmost':
        target = args[1]
        left, right = 0, len(args[0]) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if args[0][mid] == target:
                result = mid
                right = mid - 1
            elif args[0][mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result
    
    elif operation_name == 'arrBinarySearchRightmost':
        target = args[1]
        left, right = 0, len(args[0]) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if args[0][mid] == target:
                result = mid
                left = mid + 1
            elif args[0][mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    elif operation_name == 'arrClear':
        args[0].clear()
        return args[0]
    
    elif operation_name == 'arrConcat':
        return args[0] + args[1]
    
    elif operation_name == 'arrCopy':
        return args[0].copy()
    
    elif operation_name == 'arrCovariance':
        if len(args[0]) != len(args[1]) or len(args[0]) == 0:
            return 0
        mean_x = sum(args[0]) / len(args[0])
        mean_y = sum(args[1]) / len(args[1])
        return sum((x - mean_x) * (y - mean_y) for x, y in zip(args[0], args[1])) / len(args[0])
    
    elif operation_name == 'arrEvery':
        return all(args[0])
    
    elif operation_name == 'arrFill':
        return [args[1]] * args[0]
    
    elif operation_name == 'arrFirst':
        return args[0][0] if args[0] else None
    
    elif operation_name == 'arrFrom':
        return list(args[0])
    
    elif operation_name == 'arrGet':
        return args[0][args[1]] if 0 <= args[1] < len(args[0]) else None
    
    elif operation_name == 'arrIncludes':
        return args[1] in args[0]
    
    elif operation_name == 'arrIndexOf':
        try:
            return args[0].index(args[1])
        except ValueError:
            return -1
    
    elif operation_name == 'arrInsert':
        args[0].insert(args[1], args[2])
        return args[0]
    
    elif operation_name == 'arrJoin':
        return args[1].join(map(str, args[0]))
    
    elif operation_name == 'arrLast':
        return args[0][-1] if args[0] else None
    
    elif operation_name == 'arrLastIndexOf':
        return len(args[0]) - 1 - args[0][::-1].index(args[1]) if args[1] in args[0] else -1
    
    elif operation_name == 'arrMax':
        return max(args[0]) if args[0] else None
    
    elif operation_name == 'arrMedian':
        sorted_arr = sorted(args[0])
        n = len(sorted_arr)
        if n % 2 == 0:
            return (sorted_arr[n//2 - 1] + sorted_arr[n//2]) / 2
        return sorted_arr[n//2]
    
    elif operation_name == 'arrMin':
        return min(args[0]) if args[0] else None
    
    elif operation_name == 'arrMode':
        from collections import Counter
        return Counter(args[0]).most_common(1)[0][0] if args[0] else None

    elif operation_name == 'arrPercentileLinearInterpolation':
        sorted_arr = sorted(args[0])
        p = args[1]
        n = len(sorted_arr)
        r = p * (n - 1) / 100
        i = int(r)
        f = r - i
        return sorted_arr[i] + f * (sorted_arr[i + 1] - sorted_arr[i]) if i + 1 < n else sorted_arr[i]

    elif operation_name == 'arrPercentileNearestRank':
        sorted_arr = sorted(args[0])
        p = args[1]
        n = len(sorted_arr)
        r = int(round(p * (n - 1) / 100))
        return sorted_arr[r]

    elif operation_name == 'arrPercentRank':
        value = args[1]
        arr = sorted(args[0])
        return sum(1 for x in arr if x < value) * 100 / len(arr)

    elif operation_name == 'arrPop':
        return args[0].pop() if args[0] else None

    elif operation_name == 'arrPush':
        args[0].append(args[1])
        return len(args[0])

    elif operation_name == 'arrRange':
        return list(range(args[0], args[1], args[2] if len(args) > 2 else 1))

    elif operation_name == 'arrRemove':
        del args[0][args[1]]
        return args[0]

    elif operation_name == 'arrReverse':
        return args[0][::-1]

    elif operation_name == 'arrSet':
        args[0][args[1]] = args[2]
        return args[0]

    elif operation_name == 'arrShift':
        return args[0].pop(0) if args[0] else None

    elif operation_name == 'arrSize':
        return len(args[0])

    elif operation_name == 'arrSlice':
        start = args[1]
        end = args[2] if len(args) > 2 else None
        return args[0][start:end]

    elif operation_name == 'arrSome':
        return any(args[0])

    elif operation_name == 'arrSort':
        return sorted(args[0], reverse=args[1] if len(args) > 1 else False)

    elif operation_name == 'arrSortIndices':
        return sorted(range(len(args[0])), key=lambda k: args[0][k], reverse=args[1] if len(args) > 1 else False)

    elif operation_name == 'arrStandardize':
        mean = sum(args[0]) / len(args[0])
        std = (sum((x - mean) ** 2 for x in args[0]) / len(args[0])) ** 0.5
        return [(x - mean) / std for x in args[0]] if std != 0 else [0] * len(args[0])

    elif operation_name == 'arrStdev':
        mean = sum(args[0]) / len(args[0])
        return (sum((x - mean) ** 2 for x in args[0]) / len(args[0])) ** 0.5

    elif operation_name == 'arrSum':
        return sum(args[0])

    elif operation_name == 'arrUnshift':
        args[0].insert(0, args[1])
        return len(args[0])

    elif operation_name == 'arrVariance':
        mean = sum(args[0]) / len(args[0])
        return sum((x - mean) ** 2 for x in args[0]) / len(args[0])

    elif operation_name.startswith('arrNew'):
        size = args[0]
        initial_value = args[1] if len(args) > 1 else None
        
        if operation_name == 'arrNewBool':
            return [bool(initial_value)] * size if initial_value is not None else [False] * size
        elif operation_name == 'arrNewFloat':
            return [float(initial_value)] * size if initial_value is not None else [0.0] * size
        elif operation_name == 'arrNewInt':
            return [int(initial_value)] * size if initial_value is not None else [0] * size
        elif operation_name == 'arrNewString':
            return [str(initial_value)] * size if initial_value is not None else [''] * size
        elif operation_name in ['arrNewBox', 'arrayNewCol', 'arrayNewLabel', 'arrayNewLine', 'arrayNewTable']:
            return [None] * size
        elif operation_name == 'arrNewType':
            return [{}] * size

    return None




#box
def _handle_box_operation(self, operation_name, args):
    if operation_name == 'boxFunc':
        return {
            'left': args[0],
            'top': args[1],
            'right': args[2],
            'bottom': args[3],
            'border_color': args[4] if len(args) > 4 else None,
            'bg_color': args[5] if len(args) > 5 else None
        }
    
    elif operation_name == 'boxCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'boxDeleteFunc':
        return None
    
    elif operation_name == 'boxGetBottomFunc':
        return args[0]['bottom']
    
    elif operation_name == 'boxGetLeftFunc':
        return args[0]['left']
    
    elif operation_name == 'boxGetRightFunc':
        return args[0]['right']
    
    elif operation_name == 'boxGetTopFunc':
        return args[0]['top']
    
    elif operation_name == 'boxNewFunc':
        return {
            'left': 0,
            'top': 0,
            'right': 0,
            'bottom': 0,
            'border_color': None,
            'bg_color': None,
            'text': '',
            'text_color': None,
            'border_width': 1,
            'border_style': 'solid',
            'text_halign': 'center',
            'text_valign': 'middle',
            'text_font_family': 'Arial',
            'text_size': 12,
            'extend': False
        }
    
    elif operation_name == 'boxSetBgColFunc':
        args[0]['bg_color'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBorderColFunc':
        args[0]['border_color'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBorderStyleFunc':
        args[0]['border_style'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBorderWidthFunc':
        args[0]['border_width'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBottomFunc':
        args[0]['bottom'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetBottomRightPointFunc':
        args[0]['bottom'] = args[1]
        args[0]['right'] = args[2]
        return args[0]
    
    elif operation_name == 'boxSetExtendFunc':
        args[0]['extend'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetLeftFunc':
        args[0]['left'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetLeftTopFunc':
        args[0]['left'] = args[1]
        args[0]['top'] = args[2]
        return args[0]
    
    elif operation_name == 'boxSetTextFunc':
        args[0]['text'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextColFunc':
        args[0]['text_color'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextFontFamilyFunc':
        args[0]['text_font_family'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextHAlignFunc':
        args[0]['text_halign'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextSizeFunc':
        args[0]['text_size'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextVAlignFunc':
        args[0]['text_valign'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTextWrapFunc':
        args[0]['text_wrap'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTopFunc':
        args[0]['top'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetTopLeftPointFunc':
        args[0]['top'] = args[1]
        args[0]['left'] = args[2]
        return args[0]

    elif operation_name == 'boxSetRightFunc':
        args[0]['right'] = args[1]
        return args[0]
    
    elif operation_name == 'boxSetRightBottomFunc':
        args[0]['right'] = args[1]
        args[0]['bottom'] = args[2]
        return args[0]

    elif operation_name == 'boxSetTextFunc':
        args[0]['text'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextColFunc':
        args[0]['text_color'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextFontFamilyFunc':
        args[0]['text_font_family'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextHAlignFunc':
        args[0]['text_halign'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextSizeFunc':
        args[0]['text_size'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextVAlignFunc':
        args[0]['text_valign'] = args[1]
        return args[0]

    elif operation_name == 'boxSetTextWrapFunc':
        args[0]['text_wrap'] = args[1]
        return args[0]


    return None



#chart
def _handle_chart_operation(self, operation_name, args):
    if operation_name == 'chartPointCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'chartPointFromIndexFunc':
        return {
            'index': args[0],
            'price': args[1],
            'time': None,
            'bar_index': args[0],
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointFromTimeFunc':
        return {
            'time': args[0],
            'price': args[1],
            'index': None,
            'bar_index': None,
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointNewFunc':
        return {
            'time': None,
            'price': None,
            'index': None,
            'bar_index': None,
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointNowFunc':
        import time
        return {
            'time': time.time(),
            'price': args[0],
            'index': None,
            'bar_index': None,
            'offset': 0,
            'plotchar': None,
            'style': 'line',
            'color': None,
            'width': 1
        }
    
    elif operation_name == 'chartPointSetOffsetFunc':
        args[0]['offset'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetPlotCharFunc':
        args[0]['plotchar'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetStyleFunc':
        args[0]['style'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetColorFunc':
        args[0]['color'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointSetWidthFunc':
        args[0]['width'] = args[1]
        return args[0]
    
    elif operation_name == 'chartPointGetIndexFunc':
        return args[0]['index']
    
    elif operation_name == 'chartPointGetPriceFunc':
        return args[0]['price']
    
    elif operation_name == 'chartPointGetTimeFunc':
        return args[0]['time']
    
    elif operation_name == 'chartPointGetBarIndexFunc':
        return args[0]['bar_index']
    
    elif operation_name == 'chartPointGetOffsetFunc':
        return args[0]['offset']
    
    elif operation_name == 'chartPointGetStyleFunc':
        return args[0]['style']
    
    elif operation_name == 'chartPointGetColorFunc':
        return args[0]['color']
    
    elif operation_name == 'chartPointGetWidthFunc':
        return args[0]['width']

    return None



#col
def _handle_color_operation(self, operation_name, args):
    if operation_name == 'colFunc':
        return {'r': args[0], 'g': args[1], 'b': args[2], 't': args[3] if len(args) > 3 else 0}
    
    elif operation_name == 'colBFunc':
        return args[0]['b']
    
    elif operation_name == 'colFromGradientFunc':
        start_color = args[0]
        end_color = args[1]
        step = args[2]
        return {
            'r': start_color['r'] + (end_color['r'] - start_color['r']) * step,
            'g': start_color['g'] + (end_color['g'] - start_color['g']) * step,
            'b': start_color['b'] + (end_color['b'] - start_color['b']) * step,
            't': start_color['t'] + (end_color['t'] - start_color['t']) * step
        }
    
    elif operation_name == 'colGFunc':
        return args[0]['g']
    
    elif operation_name == 'colNewFunc':
        return {'r': 0, 'g': 0, 'b': 0, 't': 0}
    
    elif operation_name == 'colRFunc':
        return args[0]['r']
    
    elif operation_name == 'colRgbFunc':
        return {'r': args[0], 'g': args[1], 'b': args[2], 't': args[3] if len(args) > 3 else 0}
    
    elif operation_name == 'colTFunc':
        return args[0]['t']



#input
def _handle_input_operation(self, operation_name, args):
    if operation_name == 'inputFunc':
        return args[0]
    
    elif operation_name == 'inputBoolFunc':
        return bool(args[0])
    
    elif operation_name == 'inputColFunc':
        return args[0]
    
    elif operation_name == 'inputEnumFunc':
        options = args[1]
        default_index = args[2] if len(args) > 2 else 0
        return options[default_index]
    
    elif operation_name == 'inputFloatFunc':
        return float(args[0])
    
    elif operation_name == 'inputIntFunc':
        return int(args[0])
    
    elif operation_name == 'inputPriceFunc':
        return float(args[0])
    
    elif operation_name == 'inputSessionFunc':
        return args[0]
    
    elif operation_name == 'inputSourceFunc':
        return args[0]
    
    elif operation_name == 'inputStringFunc':
        return str(args[0])
    
    elif operation_name == 'inputSymbolFunc':
        return args[0]
    
    elif operation_name == 'inputTextAreaFunc':
        return args[0]
    
    elif operation_name == 'inputTimeFunc':
        return args[0]
    
    elif operation_name == 'inputTimeFrameFunc':
        return args[0]





#label
def _handle_label_operation(self, operation_name, args):
    if operation_name == 'labelFunc':
        return {
            'text': args[0],
            'x': args[1],
            'y': args[2],
            'color': args[3] if len(args) > 3 else None,
            'style': args[4] if len(args) > 4 else 'label_style_none',
            'textcolor': args[5] if len(args) > 5 else None,
            'size': args[6] if len(args) > 6 else 'size_auto',
            'textalign': args[7] if len(args) > 7 else 'align_center'
        }
    
    elif operation_name == 'labelCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'labelDeleteFunc':
        return None
    
    elif operation_name == 'labelGetTextFunc':
        return args[0]['text']
    
    elif operation_name == 'labelGetXFunc':
        return args[0]['x']
    
    elif operation_name == 'labelGetYFunc':
        return args[0]['y']
    
    elif operation_name == 'labelNewFunc':
        return {
            'text': '',
            'x': 0,
            'y': 0,
            'color': None,
            'style': 'label_style_none',
            'textcolor': None,
            'size': 'size_auto',
            'textalign': 'align_center',
            'tooltip': '',
            'xloc': 'xloc_bar',
            'yloc': 'yloc_price'
        }
    
    elif operation_name == 'labelSetColFunc':
        args[0]['color'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetPointFunc':
        args[0]['x'] = args[1]['x']
        args[0]['y'] = args[1]['y']
        return args[0]
    
    elif operation_name == 'labelSetSizeFunc':
        args[0]['size'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetStyleFunc':
        args[0]['style'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextFunc':
        args[0]['text'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextFontFamilyFunc':
        args[0]['font_family'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextAlignFunc':
        args[0]['textalign'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetTextColFunc':
        args[0]['textcolor'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetToolTipFunc':
        args[0]['tooltip'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetXFunc':
        args[0]['x'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetXLocFunc':
        args[0]['xloc'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetXYFunc':
        args[0]['x'] = args[1]
        args[0]['y'] = args[2]
        return args[0]
    
    elif operation_name == 'labelSetYFunc':
        args[0]['y'] = args[1]
        return args[0]
    
    elif operation_name == 'labelSetYLocFunc':
        args[0]['yloc'] = args[1]
        return args[0]



#line
def _handle_line_operation(self, operation_name, args):
    if operation_name == 'lineFunc':
        return {
            'x1': args[0],
            'y1': args[1],
            'x2': args[2],
            'y2': args[3],
            'color': args[4] if len(args) > 4 else None,
            'width': args[5] if len(args) > 5 else 1,
            'style': args[6] if len(args) > 6 else 'solid',
            'extend': False
        }
    
    elif operation_name == 'lineCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'lineDeleteFunc':
        return None
    
    elif operation_name == 'lineGetPriceFunc':
        x = args[1]
        line = args[0]
        # Linear interpolation
        if x <= line['x1']:
            return line['y1']
        if x >= line['x2']:
            return line['y2']
        ratio = (x - line['x1']) / (line['x2'] - line['x1'])
        return line['y1'] + ratio * (line['y2'] - line['y1'])
    
    elif operation_name == 'lineGetX1Func':
        return args[0]['x1']
    
    elif operation_name == 'lineGetX2Func':
        return args[0]['x2']
    
    elif operation_name == 'lineGetY1Func':
        return args[0]['y1']
    
    elif operation_name == 'lineGetY2Func':
        return args[0]['y2']
    
    elif operation_name == 'lineNewFunc':
        return {
            'x1': 0,
            'y1': 0,
            'x2': 0,
            'y2': 0,
            'color': None,
            'width': 1,
            'style': 'solid',
            'extend': False
        }
    
    elif operation_name == 'lineSetColFunc':
        args[0]['color'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetExtendFunc':
        args[0]['extend'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetFirstPointFunc':
        args[0]['x1'] = args[1]['x']
        args[0]['y1'] = args[1]['y']
        return args[0]
    
    elif operation_name == 'lineSetSecondPointFunc':
        args[0]['x2'] = args[1]['x']
        args[0]['y2'] = args[1]['y']
        return args[0]
    
    elif operation_name == 'lineSetStyleFunc':
        args[0]['style'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetWidthFunc':
        args[0]['width'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetX1Func':
        args[0]['x1'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetX2Func':
        args[0]['x2'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetXLocFunc':
        args[0]['xloc'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetXY1Func':
        args[0]['x1'] = args[1]
        args[0]['y1'] = args[2]
        return args[0]
    
    elif operation_name == 'lineSetXY2Func':
        args[0]['x2'] = args[1]
        args[0]['y2'] = args[2]
        return args[0]
    
    elif operation_name == 'lineSetY1Func':
        args[0]['y1'] = args[1]
        return args[0]
    
    elif operation_name == 'lineSetY2Func':
        args[0]['y2'] = args[1]
        return args[0]
    
    elif operation_name == 'lineFillFunc':
        return {
            'line1': args[0],
            'line2': args[1],
            'color': args[2] if len(args) > 2 else None
        }
    
    elif operation_name == 'lineFillDeleteFunc':
        return None
    
    elif operation_name == 'lineFillGetLine1Func':
        return args[0]['line1']
    
    elif operation_name == 'lineFillGetLine2Func':
        return args[0]['line2']
    
    elif operation_name == 'lineFillNewFunc':
        return {
            'line1': None,
            'line2': None,
            'color': None
        }
    
    elif operation_name == 'lineFillSetColFunc':
        args[0]['color'] = args[1]
        return args[0]




#map
def _handle_map_operation(self, operation_name, args):
    if operation_name == 'mapClearFunc':
        args[0].clear()
        return args[0]
    
    elif operation_name == 'mapContainsFunc':
        return args[1] in args[0]
    
    elif operation_name == 'mapCopyFunc':
        return dict(args[0])
    
    elif operation_name == 'mapGetFunc':
        return args[0].get(args[1])
    
    elif operation_name == 'mapKeysFunc':
        return list(args[0].keys())
    
    elif operation_name == 'mapNewTypeFunc':
        return {}
    
    elif operation_name == 'mapPutFunc':
        args[0][args[1]] = args[2]
        return args[0]
    
    elif operation_name == 'mapPutAllFunc':
        args[0].update(args[1])
        return args[0]
    
    elif operation_name == 'mapRemoveFunc':
        if args[1] in args[0]:
            del args[0][args[1]]
        return args[0]
    
    elif operation_name == 'mapSizeFunc':
        return len(args[0])
    
    elif operation_name == 'mapValuesFunc':
        return list(args[0].values())

    elif operation_name == 'mapNewBoolFunc':
        return {'type': 'bool', 'value': bool(args[0]) if args else False}
        
    elif operation_name == 'mapNewFloatFunc':
        return {'type': 'float', 'value': float(args[0]) if args else 0.0}
        
    elif operation_name == 'mapNewIntFunc':
        return {'type': 'int', 'value': int(args[0]) if args else 0}
        
    elif operation_name == 'mapNewStringFunc':
        return {'type': 'string', 'value': str(args[0]) if args else ''}




#math
def _handle_math_operation(self, operation_name, args):
    import math

    if operation_name == 'mathAbsFunc':
        return abs(args[0])
    
    elif operation_name == 'mathAcosFunc':
        return math.acos(args[0])
    
    elif operation_name == 'mathAsinFunc':
        return math.asin(args[0])
    
    elif operation_name == 'mathAtanFunc':
        return math.atan(args[0])
    
    elif operation_name == 'mathAvgFunc':
        return sum(args[0]) / len(args[0])
    
    elif operation_name == 'mathCeilFunc':
        return math.ceil(args[0])
    
    elif operation_name == 'mathCosFunc':
        return math.cos(args[0])
    
    elif operation_name == 'mathExpFunc':
        return math.exp(args[0])
    
    elif operation_name == 'mathFloorFunc':
        return math.floor(args[0])
    
    elif operation_name == 'mathLogFunc':
        return math.log(args[0])
    
    elif operation_name == 'mathLog10Func':
        return math.log10(args[0])
    
    elif operation_name == 'mathMaxFunc':
        return max(args[0])
    
    elif operation_name == 'mathMinFunc':
        return min(args[0])
    
    elif operation_name == 'mathPowFunc':
        return math.pow(args[0], args[1])
    
    elif operation_name == 'mathRandomFunc':
        return random.random()
    
    elif operation_name == 'mathRoundFunc':
        return round(args[0])
    
    elif operation_name == 'mathRoundToMinTickFunc':
        return round(args[0] / args[1]) * args[1]
    
    elif operation_name == 'mathSignFunc':
        return (1 if args[0] > 0 else -1) if args[0] != 0 else 0
    
    elif operation_name == 'mathSinFunc':
        return math.sin(args[0])
    
    elif operation_name == 'mathSqrtFunc':
        return math.sqrt(args[0])
    
    elif operation_name == 'mathSumFunc':
        return sum(args[0])
    
    elif operation_name == 'mathTanFunc':
        return math.tan(args[0])
    
    elif operation_name == 'mathToDegreesFunc':
        return math.degrees(args[0])
    
    elif operation_name == 'mathToRadiansFunc':
        return math.radians(args[0])




#matrix
def _handle_matrix_operation(self, operation_name, args):
    import numpy as np

    if operation_name == 'matrixAddColFunc':
        matrix = np.array(args[0])
        col = np.array(args[1])
        return np.column_stack((matrix, col)).tolist()
    
    elif operation_name == 'matrixAddRowFunc':
        matrix = np.array(args[0])
        row = np.array(args[1])
        return np.vstack((matrix, row)).tolist()
    
    elif operation_name == 'matrixAvgFunc':
        return np.mean(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixColFunc':
        return np.array(args[0])[:, args[1]].tolist()
    
    elif operation_name == 'matrixColumnsFunc':
        return len(np.array(args[0])[0])
    
    elif operation_name == 'matrixConcatFunc':
        return np.concatenate((np.array(args[0]), np.array(args[1]))).tolist()
    
    elif operation_name == 'matrixCopyFunc':
        return np.array(args[0]).copy().tolist()
    
    elif operation_name == 'matrixDetFunc':
        return np.linalg.det(np.array(args[0]))
    
    elif operation_name == 'matrixDiffFunc':
        return np.diff(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixEigenValuesFunc':
        return np.linalg.eigvals(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixEigenVectorsFunc':
        return np.linalg.eig(np.array(args[0]))[1].tolist()
    
    elif operation_name == 'matrixElementsCountFunc':
        return np.array(args[0]).size
    
    elif operation_name == 'matrixFillFunc':
        shape = tuple(args[0])
        value = args[1]
        return np.full(shape, value).tolist()
    
    elif operation_name == 'matrixGetFunc':
        matrix = np.array(args[0])
        row = args[1]
        col = args[2]
        return matrix[row, col]
    
    elif operation_name == 'matrixInvFunc':
        return np.linalg.inv(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixIsAntiDiagonalFunc':
        matrix = np.array(args[0])
        n = len(matrix)
        return all(matrix[i][n-1-i] != 0 for i in range(n)) and \
               all(matrix[i][j] == 0 for i in range(n) for j in range(n) if j != n-1-i)
    
    elif operation_name == 'matrixIsAntiSymmetricFunc':
        matrix = np.array(args[0])
        return np.array_equal(matrix, -matrix.T)
    
    elif operation_name == 'matrixIsBinaryFunc':
        return np.all(np.logical_or(np.array(args[0]) == 0, np.array(args[0]) == 1))
    
    elif operation_name == 'matrixIsDiagonalFunc':
        matrix = np.array(args[0])
        return np.all(matrix == np.diag(np.diag(matrix)))
    
    elif operation_name == 'matrixIsIdentityFunc':
        return np.array_equal(np.array(args[0]), np.eye(len(args[0])))
    
    elif operation_name == 'matrixIsSquareFunc':
        matrix = np.array(args[0])
        return matrix.shape[0] == matrix.shape[1]
    
    elif operation_name == 'matrixIsSymmetricFunc':
        matrix = np.array(args[0])
        return np.array_equal(matrix, matrix.T)
    
    elif operation_name == 'matrixIsTriangularFunc':
        matrix = np.array(args[0])
        return np.allclose(np.tril(matrix), matrix) or np.allclose(np.triu(matrix), matrix)
    
    elif operation_name == 'matrixIsZeroFunc':
        return np.all(np.array(args[0]) == 0)
    
    elif operation_name == 'matrixKronFunc':
        return np.kron(np.array(args[0]), np.array(args[1])).tolist()
    
    elif operation_name == 'matrixMaxFunc':
        return np.max(np.array(args[0]))
    
    elif operation_name == 'matrixMinFunc':
        return np.min(np.array(args[0]))
    
    elif operation_name == 'matrixMultFunc':
        return np.matmul(np.array(args[0]), np.array(args[1])).tolist()
    
    elif operation_name == 'matrixNewTypeFunc':
        rows = args[0]
        cols = args[1]
        return np.zeros((rows, cols)).tolist()
    
    elif operation_name == 'matrixRankFunc':
        return np.linalg.matrix_rank(np.array(args[0]))
    
    elif operation_name == 'matrixReshapeFunc':
        matrix = np.array(args[0])
        new_shape = tuple(args[1])
        return matrix.reshape(new_shape).tolist()
    
    elif operation_name == 'matrixReverseFunc':
        return np.flip(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixRowFunc':
        return np.array(args[0])[args[1]].tolist()
    
    elif operation_name == 'matrixRowsFunc':
        return len(np.array(args[0]))
    
    elif operation_name == 'matrixSetFunc':
        matrix = np.array(args[0])
        row = args[1]
        col = args[2]
        value = args[3]
        matrix[row, col] = value
        return matrix.tolist()
    
    elif operation_name == 'matrixSortFunc':
        return np.sort(np.array(args[0])).tolist()
    
    elif operation_name == 'matrixTraceFunc':
        return np.trace(np.array(args[0]))
    
    elif operation_name == 'matrixTransposeFunc':
        return np.transpose(np.array(args[0])).tolist()



#strategy
def _handle_strategy_operation(self, operation_name, args):
    if operation_name == 'strategyFunc':
        return {
            'positions': [],
            'orders': [],
            'closed_trades': [],
            'settings': {
                'initial_capital': args[0] if args else 100000,
                'commission': 0.1,
                'margin_long': 1.0,
                'margin_short': 1.0
            }
        }
    
    elif operation_name == 'strategyCancelFunc':
        order_id = args[0]
        strategy = args[1]
        strategy['orders'] = [order for order in strategy['orders'] if order['id'] != order_id]
        return strategy
    
    elif operation_name == 'strategyCancelAllFunc':
        strategy = args[0]
        strategy['orders'] = []
        return strategy
    
    elif operation_name == 'strategyCloseFunc':
        strategy = args[0]
        position_id = args[1]
        price = args[2]
        strategy['positions'] = [pos for pos in strategy['positions'] if pos['id'] != position_id]
        return strategy
    
    elif operation_name == 'strategyCloseAllFunc':
        strategy = args[0]
        price = args[1]
        strategy['positions'] = []
        return strategy
    
    elif operation_name == 'strategyEntryFunc':
        strategy = args[0]
        direction = args[1]  # 'long' or 'short'
        quantity = args[2]
        price = args[3]
        
        new_position = {
            'id': len(strategy['positions']),
            'direction': direction,
            'quantity': quantity,
            'entry_price': price,
            'entry_time': time.time(),
            'profit': 0
        }
        strategy['positions'].append(new_position)
        return strategy
    
    elif operation_name == 'strategyExitFunc':
        strategy = args[0]
        position_id = args[1]
        price = args[2]
        
        for pos in strategy['positions']:
            if pos['id'] == position_id:
                profit = (price - pos['entry_price']) * pos['quantity'] if pos['direction'] == 'long' else \
                        (pos['entry_price'] - price) * pos['quantity']
                closed_trade = {
                    'entry_price': pos['entry_price'],
                    'exit_price': price,
                    'quantity': pos['quantity'],
                    'direction': pos['direction'],
                    'profit': profit,
                    'entry_time': pos['entry_time'],
                    'exit_time': time.time()
                }
                strategy['closed_trades'].append(closed_trade)
                strategy['positions'] = [p for p in strategy['positions'] if p['id'] != position_id]
                break
        return strategy
    
    elif operation_name == 'strategyOrderFunc':
        strategy = args[0]
        order_type = args[1]  # 'limit', 'market', 'stop'
        direction = args[2]  # 'long' or 'short'
        quantity = args[3]
        price = args[4]
        
        new_order = {
            'id': len(strategy['orders']),
            'type': order_type,
            'direction': direction,
            'quantity': quantity,
            'price': price,
            'time': time.time()
        }
        strategy['orders'].append(new_order)
        return strategy




#str
def _handle_str_operation(self, operation_name, args):
    if operation_name == 'strContainsFunc':
        return args[1] in args[0]
    
    elif operation_name == 'strEndsWithFunc':
        return args[0].endswith(args[1])
    
    elif operation_name == 'strFormatFunc':
        return args[0].format(*args[1:])
    
    elif operation_name == 'strFormatTimeFunc':
        return time.strftime(args[1], time.localtime(args[0]))
    
    elif operation_name == 'strLengthFunc':
        return len(args[0])
    
    elif operation_name == 'strLowerFunc':
        return args[0].lower()
    
    elif operation_name == 'strMatchFunc':
        import re
        return bool(re.match(args[1], args[0]))
    
    elif operation_name == 'strPosFunc':
        return args[0].find(args[1])
    
    elif operation_name == 'strRepeatFunc':
        return args[0] * args[1]
    
    elif operation_name == 'strReplaceFunc':
        return args[0].replace(args[1], args[2], 1)
    
    elif operation_name == 'strReplaceAllFunc':
        return args[0].replace(args[1], args[2])
    
    elif operation_name == 'strSplitFunc':
        return args[0].split(args[1])
    
    elif operation_name == 'strStartsWithFunc':
        return args[0].startswith(args[1])
    
    elif operation_name == 'strSubstringFunc':
        return args[0][args[1]:args[2] if len(args) > 2 else None]
    
    elif operation_name == 'strToNumberFunc':
        return float(args[0])
    
    elif operation_name == 'strToStringFunc':
        return str(args[0])
    
    elif operation_name == 'strTrimFunc':
        return args[0].strip()
    
    elif operation_name == 'strUpperFunc':
        return args[0].upper()
    
    elif operation_name == 'strIndexOfFunc':
        return args[0].find(args[1], args[2] if len(args) > 2 else 0)
        
    elif operation_name == 'strLastIndexOfFunc':
        return args[0].rfind(args[1])
        
    elif operation_name == 'strCompareFunc':
        return (args[0] > args[1]) - (args[0] < args[1])
        
    elif operation_name == 'strCountFunc':
        return args[0].count(args[1])
        
    elif operation_name == 'strReverseFunc':
        return args[0][::-1]
        
    elif operation_name == 'strPadLeftFunc':
        return args[0].rjust(args[1], args[2] if len(args) > 2 else ' ')
        
    elif operation_name == 'strPadRightFunc':
        return args[0].ljust(args[1], args[2] if len(args) > 2 else ' ')




#str
def _handle_str_operation(self, operation_name, args):
    if operation_name == 'strContainsFunc':
        return args[1] in args[0]
    
    elif operation_name == 'strEndsWithFunc':
        return args[0].endswith(args[1])
    
    elif operation_name == 'strFormatFunc':
        return args[0] % tuple(args[1:])
    
    elif operation_name == 'strFormatTimeFunc':
        return args[0].strftime(args[1])
    
    elif operation_name == 'strLengthFunc':
        return len(args[0])
    
    elif operation_name == 'strLowerFunc':
        return args[0].lower()
    
    elif operation_name == 'strMatchFunc':
        import re
        return bool(re.match(args[1], args[0]))
    
    elif operation_name == 'strPosFunc':
        return args[0].find(args[1])
    
    elif operation_name == 'strRepeatFunc':
        return args[0] * args[1]
    
    elif operation_name == 'strReplaceFunc':
        return args[0].replace(args[1], args[2], 1)
    
    elif operation_name == 'strReplaceAllFunc':
        return args[0].replace(args[1], args[2])
    
    elif operation_name == 'strSplitFunc':
        return args[0].split(args[1])
    
    elif operation_name == 'strStartsWithFunc':
        return args[0].startswith(args[1])
    
    elif operation_name == 'strSubstringFunc':
        start = args[1]
        end = args[2] if len(args) > 2 else None
        return args[0][start:end]
    
    elif operation_name == 'strToNumberFunc':
        try:
            return float(args[0])
        except ValueError:
            return None
    
    elif operation_name == 'strToStringFunc':
        return str(args[0])
    
    elif operation_name == 'strTrimFunc':
        return args[0].strip()
    
    elif operation_name == 'strUpperFunc':
        return args[0].upper()

    return None



#table
def _handle_table_operation(self, operation_name, args):
    if operation_name == 'tableFunc':
        return {'rows': [], 'headers': []}
        
    elif operation_name == 'tableCellFunc':
        return {'text': args[0], 'properties': {}}
        
    elif operation_name == 'tableCellSetBgColFunc':
        args[0]['properties']['bgcolor'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetHeightFunc':
        args[0]['properties']['height'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetTextFunc':
        args[0]['text'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetTextColFunc':
        args[0]['properties']['textcolor'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetTextFontFamilyFunc':
        args[0]['properties']['fontfamily'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetTextHAlignFunc':
        args[0]['properties']['halign'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetTextSizeFunc':
        args[0]['properties']['textsize'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetTextVAlignFunc':
        args[0]['properties']['valign'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetToolTipFunc':
        args[0]['properties']['tooltip'] = args[1]
        return args[0]
        
    elif operation_name == 'tableCellSetWidthFunc':
        args[0]['properties']['width'] = args[1]
        return args[0]
        
    elif operation_name == 'tableClearFunc':
        args[0]['rows'] = []
        return args[0]
        
    elif operation_name == 'tableDeleteFunc':
        return None
        
    elif operation_name == 'tableMergeCellsFunc':
        start_row = args[1]
        end_row = args[2]
        start_col = args[3]
        end_col = args[4]
        args[0]['merged_cells'].append({
            'start_row': start_row,
            'end_row': end_row,
            'start_col': start_col,
            'end_col': end_col
        })
        return args[0]
        
    elif operation_name == 'tableNewFunc':
        return {
            'rows': [],
            'headers': [],
            'merged_cells': [],
            'properties': {}
        }
        
    elif operation_name == 'tableSetBgColFunc':
        args[0]['properties']['bgcolor'] = args[1]
        return args[0]
        
    elif operation_name == 'tableSetBorderColFunc':
        args[0]['properties']['bordercolor'] = args[1]
        return args[0]
        
    elif operation_name == 'tableSetBorderWidthFunc':
        args[0]['properties']['borderwidth'] = args[1]
        return args[0]
        
    elif operation_name == 'tableSetFrameColFunc':
        args[0]['properties']['framecolor'] = args[1]
        return args[0]
        
    elif operation_name == 'tableSetFrameWidthFunc':
        args[0]['properties']['framewidth'] = args[1]
        return args[0]
        
    elif operation_name == 'tableSetPositionFunc':
        args[0]['properties']['position'] = args[1]
        return args[0]

    return None



#weird
def _handle_weird_operation(self, operation_name, args):
    if operation_name == 'dayOfMonthFunc':
        return datetime.now().day
    
    elif operation_name == 'dayOfWeekFunc':
        return datetime.now().weekday()
    
    elif operation_name == 'fillFunc':
        return args[0]
    
    elif operation_name == 'fixNanFunc':
        return args[1] if args[0] is None or math.isnan(args[0]) else args[0]
    
    elif operation_name == 'floatFunc':
        return float(args[0])
    
    elif operation_name == 'hLineFunc':
        return {'price': args[0], 'color': args[1] if len(args) > 1 else None}
    
    elif operation_name == 'hourFunc':
        return datetime.now().hour
    
    elif operation_name == 'indicatorFunc':
        return {'name': args[0], 'parameters': args[1:]}
    
    elif operation_name == 'maxBarsBackFunc':
        return args[0]
    
    elif operation_name == 'minuteFunc':
        return datetime.now().minute
    
    elif operation_name == 'monthFunc':
        return datetime.now().month
    
    elif operation_name == 'naFunc':
        return None
    
    elif operation_name == 'nzFunc':
        return args[1] if args[0] is None else args[0]
    
    elif operation_name == 'barColFunc':
        return args[0]
    
    elif operation_name == 'bgColFunc':
        return args[0]
    
    elif operation_name == 'boolFunc':
        return bool(args[0])

    elif operation_name == 'polylineDeleteFunc':
        return None
        
    elif operation_name == 'polylineNewFunc':
        return {'points': [], 'color': args[0] if args else None}
        
    elif operation_name == 'requestCurrencyRateFunc':
        return {'currency': args[0], 'rate': args[1]}
        
    elif operation_name == 'requestDividendsFunc':
        return {'symbol': args[0], 'dividends': args[1]}
        
    elif operation_name == 'requestEarningsFunc':
        return {'symbol': args[0], 'earnings': args[1]}
        
    elif operation_name == 'requestEconomicFunc':
        return {'indicator': args[0], 'value': args[1]}
        
    elif operation_name == 'requestFinancialFunc':
        return {'symbol': args[0], 'data': args[1]}
        
    elif operation_name == 'requestQuandlFunc':
        return {'code': args[0], 'data': args[1]}
        
    elif operation_name == 'requestSecurityFunc':
        return {'symbol': args[0], 'data': args[1]}
        
    elif operation_name == 'requestSecurityLowerTfFunc':
        return {'symbol': args[0], 'timeframe': args[1], 'data': args[2]}
        
    elif operation_name == 'requestSeedFunc':
        return args[0]
        
    elif operation_name == 'requestSplitsFunc':
        return {'symbol': args[0], 'splits': args[1]}
        
    elif operation_name == 'runtimeErrorFunc':
        raise RuntimeError(args[0])
        
    elif operation_name == 'secondFunc':
        return datetime.now().second





#ta functions
def _handle_ta_operation(self, operation_name, args):
    if operation_name == 'taAlmaFunc':
        return self._calculate_alma(args[0], args[1], args[2], args[3])
        
    elif operation_name == 'taAtrFunc':
        return self._calculate_atr(args[0], args[1], args[2], args[3])
        
    elif operation_name == 'taBarsSinceFunc':
        return self._calculate_bars_since(args[0])
        
    elif operation_name == 'taBbFunc':
        return self._calculate_bollinger_bands(args[0], args[1], args[2])
        
    elif operation_name == 'taBbwFunc':
        return self._calculate_bb_width(args[0], args[1], args[2])
        
    elif operation_name == 'taCciFunc':
        return self._calculate_cci(args[0], args[1])
        
    elif operation_name == 'taChangeFunc':
        return self._calculate_change(args[0])
        
    elif operation_name == 'taCmoFunc':
        return self._calculate_cmo(args[0], args[1])
        
    elif operation_name == 'taCogFunc':
        return self._calculate_cog(args[0], args[1])
        
    elif operation_name == 'taCorrelationFunc':
        return self._calculate_correlation(args[0], args[1], args[2])
        
    elif operation_name == 'taCrossFunc':
        return self._check_cross(args[0], args[1])
        
    elif operation_name == 'taCrossoverFunc':
        return self._check_crossover(args[0], args[1])
        
    elif operation_name == 'taCrossunderFunc':
        return self._check_crossunder(args[0], args[1])
        
    elif operation_name == 'taCumFunc':
        return self._calculate_cumulative(args[0])
        
    elif operation_name == 'taDevFunc':
        return self._calculate_deviation(args[0], args[1])
        
    elif operation_name == 'taDmiFunc':
        return self._calculate_dmi(args[0], args[1])
        
    elif operation_name == 'taEmaFunc':
        return self._calculate_ema(args[0], args[1])
        
    elif operation_name == 'taFallingFunc':
        return self._check_falling(args[0], args[1])
        
    elif operation_name == 'taHighestFunc':
        return self._find_highest(args[0], args[1])
        
    elif operation_name == 'taHighestBarsFunc':
        return self._find_highest_bars(args[0], args[1])
        
    elif operation_name == 'taHmaFunc':
        return self._calculate_hma(args[0], args[1])
        
    elif operation_name == 'taKcFunc':
        return self._calculate_keltner_channels(args[0], args[1], args[2])
        
    elif operation_name == 'taKcwFunc':
        return self._calculate_kc_width(args[0], args[1], args[2])
        
    elif operation_name == 'taLinRegFunc':
        return self._calculate_linear_regression(args[0], args[1])
        
    elif operation_name == 'taLowestFunc':
        return self._find_lowest(args[0], args[1])
        
    elif operation_name == 'taLowestBarsFunc':
        return self._find_lowest_bars(args[0], args[1])
        
    elif operation_name == 'taMacdFunc':
        return self._calculate_macd(args[0], args[1], args[2], args[3])
        
    elif operation_name == 'taMaxFunc':
        return self._calculate_max(args[0], args[1])
        
    elif operation_name == 'taMedianFunc':
        return self._calculate_median(args[0], args[1])
        
    elif operation_name == 'taMfiFunc':
        return self._calculate_mfi(args[0], args[1], args[2], args[3], args[4])
        
    elif operation_name == 'taMinFunc':
        return self._calculate_min(args[0], args[1])
        
    elif operation_name == 'taModeFunc':
        return self._calculate_mode(args[0], args[1])
        
    elif operation_name == 'taMomFunc':
        return self._calculate_momentum(args[0], args[1])
        
    elif operation_name == 'taPercentileLinearInterpolationFunc':
        return self._calculate_percentile_linear(args[0], args[1], args[2])
        
    elif operation_name == 'taPercentileNearestRankFunc':
        return self._calculate_percentile_rank(args[0], args[1], args[2])
        
    elif operation_name == 'taPercentRankFunc':
        return self._calculate_percent_rank(args[0], args[1])
        
    elif operation_name == 'taPivotPointLevelsFunc':
        return self._calculate_pivot_points(args[0], args[1], args[2], args[3])
        
    elif operation_name == 'taPivotHighFunc':
        return self._find_pivot_high(args[0], args[1], args[2])
        
    elif operation_name == 'taPivotLowFunc':
        return self._find_pivot_low(args[0], args[1], args[2])
        
    elif operation_name == 'taRangeFunc':
        return self._calculate_range(args[0], args[1])
        
    elif operation_name == 'taRisingFunc':
        return self._check_rising(args[0], args[1])
        
    elif operation_name == 'taRmaFunc':
        return self._calculate_rma(args[0], args[1])
        
    elif operation_name == 'taRocFunc':
        return self._calculate_roc(args[0], args[1])
        
    elif operation_name == 'taRsiFunc':
        return self._calculate_rsi(args[0], args[1])
        
    elif operation_name == 'taSarFunc':
        return self._calculate_sar(args[0], args[1], args[2], args[3])
        
    elif operation_name == 'taSmaFunc':
        return self._calculate_sma(args[0], args[1])
        
    elif operation_name == 'taStdevFunc':
        return self._calculate_stdev(args[0], args[1])
        
    elif operation_name == 'taStochFunc':
        return self._calculate_stoch(args[0], args[1], args[2], args[3], args[4])
        
    elif operation_name == 'taSuperTrendFunc':
        return self._calculate_supertrend(args[0], args[1], args[2])
        
    elif operation_name == 'taSwmaFunc':
        return self._calculate_swma(args[0])
        
    elif operation_name == 'taTrFunc':
        return self._calculate_true_range(args[0], args[1], args[2])
        
    elif operation_name == 'taTsiFunc':
        return self._calculate_tsi(args[0], args[1], args[2])
        
    elif operation_name == 'taValueWhenFunc':
        return self._get_value_when(args[0], args[1])
        
    elif operation_name == 'taVarianceFunc':
        return self._calculate_variance(args[0], args[1])
        
    elif operation_name == 'taVwapFunc':
        return self._calculate_vwap(args[0], args[1], args[2])
        
    elif operation_name == 'taVwmaFunc':
        return self._calculate_vwma(args[0], args[1], args[2])
        
    elif operation_name == 'taWmaFunc':
        return self._calculate_wma(args[0], args[1])
        
    elif operation_name == 'taWprFunc':
        return self._calculate_wpr(args[0], args[1], args[2], args[3])

    return None



                                                     #More calculatiosn for TA#



def _calculate_alma(self, source, period, offset, sigma):
    """Arnaud Legoux Moving Average"""
    m = offset * (period - 1)
    s = period / sigma
    weights = [np.exp(-((i - m) ** 2) / (2 * s * s)) for i in range(period)]
    weight_sum = sum(weights)
    weights = [w / weight_sum for w in weights]
    return sum(s * w for s, w in zip(source[-period:], weights))

def _calculate_atr(self, high, low, close, period):
    """Average True Range"""
    tr = [max(high[i] - low[i], 
             abs(high[i] - close[i-1]), 
             abs(low[i] - close[i-1])) 
          for i in range(1, len(high))]
    return self._calculate_rma(tr, period)

def _calculate_bars_since(self, condition):
    """Bars Since Condition"""
    count = 0
    for i in reversed(range(len(condition))):
        if condition[i]:
            return count
        count += 1
    return count

def _calculate_bollinger_bands(self, source, period, multiplier):
    """Bollinger Bands"""
    sma = self._calculate_sma(source, period)
    std = self._calculate_stdev(source, period)
    upper = sma + multiplier * std
    lower = sma - multiplier * std
    return {'middle': sma, 'upper': upper, 'lower': lower}

def _calculate_bb_width(self, source, period, multiplier):
    """Bollinger Bandwidth"""
    bb = self._calculate_bollinger_bands(source, period, multiplier)
    return (bb['upper'] - bb['lower']) / bb['middle']

def _calculate_cci(self, high, low, close, period):
    """Commodity Channel Index"""
    tp = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    sma = self._calculate_sma(tp, period)
    mean_deviation = sum(abs(tp[-i] - sma) for i in range(1, period + 1)) / period
    return (tp[-1] - sma) / (0.015 * mean_deviation)

def _calculate_cmo(self, source, period):
    """Chande Momentum Oscillator"""
    changes = [source[i] - source[i-1] for i in range(1, len(source))]
    gains = sum(c for c in changes[-period:] if c > 0)
    losses = abs(sum(c for c in changes[-period:] if c < 0))
    return 100 * (gains - losses) / (gains + losses) if (gains + losses) != 0 else 0

def _calculate_dmi(self, high, low, close, period):
    """Directional Movement Index"""
    tr = self._calculate_atr(high, low, close, period)
    plus_dm = [max(high[i] - high[i-1], 0) if (high[i] - high[i-1]) > (low[i-1] - low[i]) else 0 
               for i in range(1, len(high))]
    minus_dm = [max(low[i-1] - low[i], 0) if (low[i-1] - low[i]) > (high[i] - high[i-1]) else 0 
                for i in range(1, len(high))]
    
    plus_di = 100 * self._calculate_rma(plus_dm, period) / tr
    minus_di = 100 * self._calculate_rma(minus_dm, period) / tr
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di) if (plus_di + minus_di) != 0 else 0
    adx = self._calculate_rma([dx], period)
    
    return {'plus_di': plus_di, 'minus_di': minus_di, 'adx': adx}

def _calculate_ema(self, source, period):
    """Exponential Moving Average"""
    alpha = 2 / (period + 1)
    ema = source[0]
    for price in source[1:]:
        ema = alpha * price + (1 - alpha) * ema
    return ema

def _calculate_hma(self, source, period):
    """Hull Moving Average"""
    wma1 = self._calculate_wma(source, period // 2)
    wma2 = self._calculate_wma(source, period)
    diff = [2 * w1 - w2 for w1, w2 in zip(wma1, wma2)]
    return self._calculate_wma(diff, int(np.sqrt(period)))

def _calculate_keltner_channels(self, source, period, multiplier):
    """Keltner Channels"""
    ema = self._calculate_ema(source, period)
    atr = self._calculate_atr(high, low, close, period)
    upper = ema + multiplier * atr
    lower = ema - multiplier * atr
    return {'middle': ema, 'upper': upper, 'lower': lower}

def _calculate_mfi(self, high, low, close, volume, period):
    """Money Flow Index"""
    tp = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    mf = [tp[i] * volume[i] for i in range(len(tp))]
    
    positive_mf = sum(mf[i] for i in range(1, period + 1) if tp[i] > tp[i-1])
    negative_mf = sum(mf[i] for i in range(1, period + 1) if tp[i] < tp[i-1])
    
    return 100 - (100 / (1 + positive_mf / negative_mf)) if negative_mf != 0 else 100

def _calculate_pivot_points(self, high, low, close, pivot_type='standard'):
    """Pivot Points"""
    if pivot_type == 'standard':
        pp = (high[-1] + low[-1] + close[-1]) / 3
        r1 = 2 * pp - low[-1]
        s1 = 2 * pp - high[-1]
        r2 = pp + (high[-1] - low[-1])
        s2 = pp - (high[-1] - low[-1])
        r3 = high[-1] + 2 * (pp - low[-1])
        s3 = low[-1] - 2 * (high[-1] - pp)
        
        return {
            'pp': pp,
            'r1': r1, 's1': s1,
            'r2': r2, 's2': s2,
            'r3': r3, 's3': s3
        }

def _calculate_stdev(self, source, period):
    """Standard Deviation"""
    mean = sum(source[-period:]) / period
    squared_diff = [(x - mean) ** 2 for x in source[-period:]]
    return np.sqrt(sum(squared_diff) / period)

#

def _calculate_wpr(self, high, low, close, period):
    """Williams Percent Range"""
    highest_high = max(high[-period:])
    lowest_low = min(low[-period:])
    return ((highest_high - close[-1]) / (highest_high - lowest_low)) * -100

def _calculate_wma(self, source, period):
    """Weighted Moving Average"""
    weights = list(range(1, period + 1))
    wma = sum(source[-period:] * weights) / sum(weights)
    return wma

def _calculate_vwma(self, source, volume, period):
    """Volume Weighted Moving Average"""
    return sum(source[-period:] * volume[-period:]) / sum(volume[-period:])

def _calculate_vwap(self, price, volume, period):
    """Volume Weighted Average Price"""
    return sum(price[-period:] * volume[-period:]) / sum(volume[-period:])

def _calculate_variance(self, source, period):
    """Variance"""
    mean = sum(source[-period:]) / period
    return sum((x - mean) ** 2 for x in source[-period:]) / period

def _calculate_tsi(self, source, short_period, long_period):
    """True Strength Index"""
    momentum = [source[i] - source[i-1] for i in range(1, len(source))]
    abs_momentum = [abs(m) for m in momentum]
    
    smooth1 = self._calculate_ema(momentum, long_period)
    smooth2 = self._calculate_ema(smooth1, short_period)
    abs_smooth1 = self._calculate_ema(abs_momentum, long_period)
    abs_smooth2 = self._calculate_ema(abs_smooth1, short_period)
    
    return (smooth2 / abs_smooth2) * 100

def _calculate_true_range(self, high, low, close):
    """True Range"""
    tr1 = high - low
    tr2 = abs(high - close[-1])
    tr3 = abs(low - close[-1])
    return max(tr1, tr2, tr3)

def _calculate_swma(self, source):
    """Symmetrically Weighted Moving Average"""
    weights = [1, 2, 2, 1]
    return sum(s * w for s, w in zip(source[-4:], weights)) / sum(weights)

def _calculate_supertrend(self, high, low, close, period, multiplier):
    """SuperTrend"""
    atr = self._calculate_atr(high, low, close, period)
    basic_upperband = (high + low) / 2 + multiplier * atr
    basic_lowerband = (high + low) / 2 - multiplier * atr
    
    return {'upperband': basic_upperband, 'lowerband': basic_lowerband}

def _calculate_stoch(self, high, low, close, k_period, d_period):
    """Stochastic Oscillator"""
    lowest_low = min(low[-k_period:])
    highest_high = max(high[-k_period:])
    k = ((close[-1] - lowest_low) / (highest_high - lowest_low)) * 100
    d = self._calculate_sma([k], d_period)
    return {'k': k, 'd': d}

def _calculate_sma(self, source, period):
    """Simple Moving Average"""
    return sum(source[-period:]) / period

def _calculate_rsi(self, source, period):
    """Relative Strength Index"""
    gains = [max(source[i] - source[i-1], 0) for i in range(1, len(source))]
    losses = [max(source[i-1] - source[i], 0) for i in range(1, len(source))]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def _calculate_roc(self, source, period):
    """Rate of Change"""
    return ((source[-1] - source[-period]) / source[-period]) * 100

def _calculate_rma(self, source, period):
    """Running Moving Average"""
    alpha = 1.0 / period
    rma = source[0]
    for value in source[1:]:
        rma = alpha * value + (1 - alpha) * rma
    return rma

def _calculate_macd(self, source, fast_period, slow_period, signal_period):
    """Moving Average Convergence Divergence"""
    fast_ema = self._calculate_ema(source, fast_period)
    slow_ema = self._calculate_ema(source, slow_period)
    macd_line = fast_ema - slow_ema
    signal_line = self._calculate_ema([macd_line], signal_period)
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }

def _calculate_linear_regression(self, source, period):
    """Linear Regression"""
    x = np.arange(period)
    y = np.array(source[-period:])
    slope, intercept = np.polyfit(x, y, 1)
    return slope * (period - 1) + intercept

def _calculate_correlation(self, source1, source2, period):
    """Correlation Coefficient"""
    x = np.array(source1[-period:])
    y = np.array(source2[-period:])
    return np.corrcoef(x, y)[0, 1]

def _check_cross(self, source1, source2):
    """Cross Detection"""
    return (source1[-2] <= source2[-2] and source1[-1] > source2[-1]) or \
           (source1[-2] >= source2[-2] and source1[-1] < source2[-1])

def _check_crossover(self, source1, source2):
    """Crossover Detection"""
    return source1[-2] <= source2[-2] and source1[-1] > source2[-1]

def _check_crossunder(self, source1, source2):
    """Crossunder Detection"""
    return source1[-2] >= source2[-2] and source1[-1] < source2[-1]

def _calculate_cumulative(self, source):
    """Cumulative Sum"""
    return np.cumsum(source)

def _calculate_deviation(self, source, period):
    """Deviation from Moving Average"""
    sma = self._calculate_sma(source, period)
    return [x - sma for x in source[-period:]]

def _check_falling(self, source, period):
    """Falling Detection"""
    return all(source[i] > source[i+1] for i in range(-period, -1))

def _find_highest(self, source, period):
    """Highest Value"""
    return max(source[-period:])

def _find_highest_bars(self, source, period):
    """Bars since Highest Value"""
    highest = max(source[-period:])
    for i in range(len(source[-period:])):
        if source[-i-1] == highest:
            return i
    return period

def _find_lowest(self, source, period):
    """Lowest Value"""
    return min(source[-period:])

def _find_lowest_bars(self, source, period):
    """Bars since Lowest Value"""
    lowest = min(source[-period:])
    for i in range(len(source[-period:])):
        if source[-i-1] == lowest:
            return i
    return period

def _calculate_mode(self, source, period):
    """Mode Value"""
    return stats.mode(source[-period:])[0]

def _calculate_momentum(self, source, period):
    """Momentum"""
    return source[-1] - source[-period]

def _calculate_percentile_linear(self, source, period, percent):
    """Percentile with Linear Interpolation"""
    return np.percentile(source[-period:], percent, interpolation='linear')

def _calculate_percentile_rank(self, source, period, percent):
    """Percentile with Nearest Rank"""
    return np.percentile(source[-period:], percent, interpolation='nearest')

def _calculate_percent_rank(self, source, period):
    """Percent Rank"""
    current = source[-1]
    history = source[-period:]
    return sum(1 for x in history if x <= current) / period * 100

def _find_pivot_high(self, high, left_bars, right_bars):
    """Pivot High"""
    for i in range(left_bars, len(high)-right_bars):
        if all(high[i] > high[j] for j in range(i-left_bars, i)) and \
           all(high[i] > high[j] for j in range(i+1, i+right_bars+1)):
            return high[i]
    return None

def _find_pivot_low(self, low, left_bars, right_bars):
    """Pivot Low"""
    for i in range(left_bars, len(low)-right_bars):
        if all(low[i] < low[j] for j in range(i-left_bars, i)) and \
           all(low[i] < low[j] for j in range(i+1, i+right_bars+1)):
            return low[i]
    return None

def _calculate_range(self, high, low, period):
    """Price Range"""
    return [h - l for h, l in zip(high[-period:], low[-period:])]

def _check_rising(self, source, period):
    """Rising Detection"""
    return all(source[i] < source[i+1] for i in range(-period, -1))

def _get_value_when(self, condition, source):
    """Value When Condition"""
    for i in reversed(range(len(condition))):
        if condition[i]:
            return source[i]
    return None

def _calculate_cog(self, source, period):
    """Center of Gravity Oscillator"""
    weights = range(1, period + 1)
    weighted_sum = sum(source[-i] * i for i in range(1, period + 1))
    total_sum = sum(source[-period:])
    return -weighted_sum / total_sum if total_sum != 0 else 0

def _calculate_change(self, source):
    """Price Change"""
    return source[-1] - source[-2]

def _calculate_sar(self, high, low, acceleration=0.02, maximum=0.2):
    """Parabolic SAR"""
    trend = 1  # 1 for uptrend, -1 for downtrend
    sar = low[0]
    ep = high[0]  # Extreme point
    acc = acceleration
    
    result = []
    for i in range(1, len(high)):
        sar = sar + acc * (ep - sar)
        
        if trend == 1:
            if low[i] < sar:
                trend = -1
                sar = max(high[i-1], high[i])
                ep = low[i]
                acc = acceleration
            else:
                if high[i] > ep:
                    ep = high[i]
                    acc = min(acc + acceleration, maximum)
        else:
            if high[i] > sar:
                trend = 1
                sar = min(low[i-1], low[i])
                ep = high[i]
                acc = acceleration
            else:
                if low[i] < ep:
                    ep = low[i]
                    acc = min(acc + acceleration, maximum)
                    
        result.append(sar)
    return result

def _calculate_kc_width(self, source, period, multiplier):
    """Keltner Channel Width"""
    kc = self._calculate_keltner_channels(source, period, multiplier)
    return (kc['upper'] - kc['lower']) / kc['middle']

def _calculate_max(self, source1, source2):
    """Maximum of Two Series"""
    return [max(a, b) for a, b in zip(source1, source2)]

def _calculate_min(self, source1, source2):
    """Minimum of Two Series"""
    return [min(a, b) for a, b in zip(source1, source2)]

def _calculate_tr(self, high, low, close):
    """True Range"""
    tr = []
    for i in range(1, len(high)):
        tr.append(max(
            high[i] - low[i],
            abs(high[i] - close[i-1]),
            abs(low[i] - close[i-1])
        ))
    return tr

def _calculate_median(self, source, period):
    """Median Value"""
    return np.median(source[-period:])

def _calculate_standardize(self, source, period):
    """Standardize Series"""
    mean = self._calculate_sma(source, period)
    std = self._calculate_stdev(source, period)
    return [(x - mean) / std if std != 0 else 0 for x in source[-period:]]





"""---------------------------------------------------------------------------------------------------------------------------------------------"""





#suggest improvements#
# 1. Error handling and input validation
def validate_ta_input(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, (list, np.ndarray)):
                if len(arg) == 0:
                    raise ValueError(f"Empty input array in {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

# 2. Caching implementation
class TACache:
    def __init__(self):
        self.cache = {}
        
    def get(self, key):
        return self.cache.get(key)
        
    def set(self, key, value):
        self.cache[key] = value
        
    def clear(self):
        self.cache.clear()

# 3. Vectorized operations
def vectorized_calculations(self):
    @np.vectorize
    def calculate_indicators(source, period):
        return self._calculate_ta_indicator(source, period)

# 4. Type hints and documentation
from typing import List, Union, Optional, Dict
import numpy.typing as npt

class TechnicalAnalysis:
    def calculate_indicator(
        self, 
        source: Union[List[float], npt.NDArray], 
        period: int
    ) -> Dict[str, float]:
        """
        Calculates technical indicator values
        
        Args:
            source: Price/volume data
            period: Calculation period
            
        Returns:
            Dictionary containing indicator values
        """
        pass

# 5. Memory optimization
class DataManager:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.data = deque(maxlen=max_size)
        
    def add_data(self, value):
        self.data.append(value)
        
    def get_data(self, period: int):
        return list(self.data)[-period:]

# 6. Progress tracking
class ProgressTracker:
    def __init__(self, total_steps: int):
        self.total = total_steps
        self.current = 0
        
    def update(self, steps: int = 1):
        self.current += steps
        self._display_progress()
        
    def _display_progress(self):
        percentage = (self.current / self.total) * 100
        print(f"Progress: {percentage:.1f}%")

# 7. Logging implementation
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('TechnicalAnalysis')

# 8. Custom indicator support
class CustomIndicator:
    def __init__(self, calculation_func):
        self.calc_func = calculation_func
        
    def calculate(self, *args, **kwargs):
        return self.calc_func(*args, **kwargs)

# 9. Parallel processing
from concurrent.futures import ThreadPoolExecutor

class ParallelProcessor:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
    def process_indicators(self, calculations):
        futures = []
        for calc in calculations:
            futures.append(
                self.executor.submit(calc['func'], *calc['args'])
            )
        return [f.result() for f in futures]

# Integration with main interpreter
class Interpreter:
    def __init__(self):
        self.ta_cache = TACache()
        self.data_manager = DataManager()
        self.progress_tracker = ProgressTracker(100)
        self.parallel_processor = ParallelProcessor()
        
    def calculate_technical_indicators(self, source, indicators):
        logger.info("Starting technical analysis calculations")
        
        results = {}
        calculations = []
        
        for indicator in indicators:
            cached_result = self.ta_cache.get(indicator)
            if cached_result:
                results[indicator] = cached_result
                continue
                
            calculations.append({
                'func': self._get_indicator_function(indicator),
                'args': (source,)
            })
        
        parallel_results = self.parallel_processor.process_indicators(calculations)
        
        for indicator, result in zip(indicators, parallel_results):
            self.ta_cache.set(indicator, result)
            results[indicator] = result
            
        logger.info("Completed technical analysis calculations")
        return results



"""---------------------------------------------------------------------------------------------------------------------------------------------"""




#suggestion calculations#


# Data Management Functions
class DataQueue:
    def __init__(self, maxlen=1000):
        self.queue = deque(maxlen=maxlen)
        
    def push(self, data):
        self.queue.append(data)
        
    def get_window(self, size):
        return list(self.queue)[-size:]
        
    def clear(self):
        self.queue.clear()

class DataTracker:
    def __init__(self):
        self.data_points = []
        self.timestamps = []
        
    def add_point(self, value, timestamp):
        self.data_points.append(value)
        self.timestamps.append(timestamp)
        
    def get_range(self, start_time, end_time):
        mask = [(t >= start_time) and (t <= end_time) for t in self.timestamps]
        return [d for d, m in zip(self.data_points, mask) if m]

# Progress Tracking Functions
class DetailedProgress:
    def __init__(self, total_steps, description=""):
        self.total = total_steps
        self.current = 0
        self.description = description
        self.start_time = time.time()
        
    def update(self, steps=1):
        self.current += steps
        self._show_detailed_progress()
        
    def _show_detailed_progress(self):
        elapsed = time.time() - self.start_time
        percentage = (self.current / self.total) * 100
        remaining = (elapsed / self.current) * (self.total - self.current) if self.current > 0 else 0
        print(f"{self.description}: {percentage:.1f}% | Time remaining: {remaining:.1f}s")

# Cache Management Functions
class IndicatorCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}
        
    def get(self, key):
        if key in self.cache:
            self.access_count[key] += 1
            return self.cache[key]
        return None
        
    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            least_used = min(self.access_count.items(), key=lambda x: x[1])[0]
            del self.cache[least_used]
            del self.access_count[least_used]
        self.cache[key] = value
        self.access_count[key] = 1

# Performance Monitoring Functions
class PerformanceMonitor:
    def __init__(self):
        self.start_times = {}
        self.execution_times = {}
        
    def start(self, operation):
        self.start_times[operation] = time.time()
        
    def stop(self, operation):
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            self.execution_times[operation] = duration
            del self.start_times[operation]
            
    def get_stats(self):
        return self.execution_times

# Parallel Processing Functions
class TaskManager:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks = []
        
    def add_task(self, func, *args):
        self.tasks.append((func, args))
        
    def execute_all(self):
        futures = []
        for func, args in self.tasks:
            futures.append(self.executor.submit(func, *args))
        return [f.result() for f in futures]

# Data Validation Functions
class DataValidator:
    @staticmethod
    def validate_numeric_array(arr):
        return all(isinstance(x, (int, float)) for x in arr)
        
    @staticmethod
    def validate_period(period, data_length):
        return 0 < period <= data_length
        
    @staticmethod
    def validate_indicator_inputs(source, period):
        if not source or len(source) < period:
            raise ValueError("Invalid input length or period")
        if not DataValidator.validate_numeric_array(source):
            raise ValueError("Source must contain numeric values")

# Custom Indicator Builder
class IndicatorBuilder:
    def __init__(self):
        self.calculations = []
        
    def add_calculation(self, func):
        self.calculations.append(func)
        
    def build(self, source):
        result = source
        for calc in self.calculations:
            result = calc(result)
        return result

# Memory Management Functions
class MemoryManager:
    def __init__(self, max_memory_mb=100):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.allocated = {}
        
    def allocate(self, name, size):
        if self.get_total_allocated() + size > self.max_memory:
            self.cleanup()
        self.allocated[name] = size
        
    def cleanup(self):
        self.allocated.clear()
        
    def get_total_allocated(self):
        return sum(self.allocated.values())

# Logging Enhancement Functions
class EnhancedLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.setup_logging()
        
    def setup_logging(self):
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler = logging.FileHandler('technical_analysis.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def log_calculation(self, indicator, params):
        self.logger.info(f"Calculating {indicator} with params: {params}")
        
    def log_error(self, error):
        self.logger.error(f"Error occurred: {str(error)}")

# Result Formatter Functions
class ResultFormatter:
    @staticmethod
    def format_indicator_result(result, decimals=4):
        if isinstance(result, dict):
            return {k: round(v, decimals) for k, v in result.items()}
        elif isinstance(result, (list, np.ndarray)):
            return [round(x, decimals) for x in result]
        elif isinstance(result, (int, float)):
            return round(result, decimals)
        return result


"""---------------------------------------------------------------------------------------------------------------------------------------------"""


#final evaluation#
def evaluate_with_env(self, env):
        self.environment = env
        return self._evaluate(self.ast)

def interpret(source_code):
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    print("Tokens:", tokens) # For debugging
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast) # For debugging
    
    evaluator = Evaluator(ast)
    result = evaluator.evaluate()
    
    return result
