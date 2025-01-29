import re
from typing import Any, Dict, List, Optional, Tuple, Union
import math
import numpy as np
import talib

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
                    if identifier in ['open', 'high', 'low', 'close', 'volume', 'hl2', 'hlc3', 'hlcc4', 'ohlc4','symInfoMinMove', 'symInfoMinTick', 'symInfoPointValue', 'symInfoPrefix','symInfoPriceScale', 'symInfoRoot', 'symInfoSector', 'symInfoSession','symInfoShareholders', 'symInfoSharesOutstandingFloat','symInfoSharesOutstandingTotal',             'sma', 'ema', 'rsi', 'minvalue', 'maxvalue', 'taAccDist', 'taIII', 'taNVI', 'taOBV', 'taPVI', 'taPVT', 'taTR', 'taVWAP','taWAD', 'taWVAD', 'taAlma', 'taAtr', 'taBarsSince', 'taBb', 'taBbw', 'taCci','taChange', 'taCmo', 'taCog', 'taCorrelation', 'taCross', 'taCrossover','taCrossunder', 'taCum', 'taDev', 'taDmi', 'taEma', 'taFalling', 'taHighest','taHighestBars', 'taHma', 'taKc', 'taKcw', 'taLinReg', 'taLowest','taLowestBars', 'taMacd', 'taMax', 'taMedian', 'taMfi', 'taMin', 'taMode','taMom', 'taPercentile', 'taPercentRank', 'taPivotHigh', 'taPivotLow','taRange', 'taRising', 'taRma', 'taRoc', 'taRsi', 'taSar', 'taSma', 'taStdev','taStoch', 'taSuperTrend', 'taSwma', 'taTsi', 'taValueWhen', 'taVariance','taVwap', 'taVwma', 'taWma', 'taWpr', 'strategyAccountCurrency', 'strategyAvgLosingTrade','strategyAvgLosingTradePercent', 'strategyAvgTrade','strategyAvgTradePercent', 'strategyAvgWinningTrade','strategyAvgWinningTradePercent', 'strategyClosedTrades','strategyClosedTradesFirstIndex', 'strategyEquity', 'strategyEvenTrades','strategyGrossLoss', 'strategyGrossLossPercent', 'strategyGrossProfit','strategyGrossProfitPercent', 'strategyInitialCapital', 'strategyLossTrades','strategyMarginLiquidationPrice', 'strategyMaxContractsHeldAll','strategyMaxContractsHeldLong', 'strategyMaxContractsHeldShort','strategyMaxDrawdown', 'strategyMaxDrawdownPercent', 'strategyMaxRunup','strategyMaxRunupPercent', 'strategyNetProfit', 'strategyNetProfitPercent','strategyOpenProfit', 'strategyOpenProfitPercent', 'strategyOpenTrades','strategyOpenTradesCapitalHeld', 'strategyPositionAvgPrice','strategyPositionEntryName', 'strategyPositionSize', 'strategyWinTrades',             'dayOfMonth', 'dayOfWeek', 'hour', 'minute', 'month','second', 'time', 'timeClose', 'timeTradingDay', 'timeNow','weekOfYear', 'year', 'sessionIsFirstBar', 'sessionIsFirstBarRegular','sessionIsLastBar', 'sessionIsLastBarRegular', 'sessionIsMarket','sessionIsPostMarket', 'sessionIsPreMarket',             'boxAll', 'chartBgCol', 'chartFgCol', 'chartIsHeikinAshi','chartIsKagi', 'chartIsLineBreak', 'chartIsPnf', 'chartIsRange','chartIsRenko', 'chartIsStandard', 'chartLeftVisibleBarTime','chartRightVisibleBarTime', 'labelAll', 'lineAll', 'lineFillAll','polylineAll', 'tableAll', 'andOp', 'enumType', 'exportFunc', 'forLoop', 'forInLoop', 'ifCond', 'importFunc', 'methodFunc', 'notOp', 'orOp', 'switchCase', 'typeDef', 'let', 'letip', 'whileLoop','open','high','low','close','volume','barIndex','barStateIsConfirmed','barStateIsFirst','barStateIsHistory','barStateIsLast','barStateIsLastConfirmedHistory','barStateIsNew','barStateIsRealtime','boxAll','chartBgCol','chartFgCol','chartIsHeikinAshi','chartIsKagi','chartIsLineBreak','chartIsPnf','chartIsRange','chartIsRenko','chartIsStandard','chartLeftVisibleBarTime','chartRightVisibleBarTime','dayOfMonth','dayOfWeek','dividendsFutureAmount','dividendsFutureExDate','dividendsFuturePayDate','earningsFutureEps','earningsFuturePeriodEndTime','earningsFutureRevenue','earningsFutureTime','hl2','hlc3','hlcc4','hour','labelAll','lastBarIndex','lastBarTime','lineAll','lineFillAll','minute','month','na','ohlc4','polylineAll','second','sessionIsFirstBar','sessionIsFirstBarRegular','sessionIsLastBar','sessionIsLastBarRegular','sessionIsMarket','sessionIsPostMarket','sessionIsPreMarket','strategyAccountCurrency','strategyAvgLosingTrade','strategyAvgLosingTradePercent','strategyAvgTrade','strategyAvgTradePercent','strategyAvgWinningTrade','strategyAvgWinningTradePercent','strategyClosedTrades','strategyClosedTradesFirstIndex','strategyEquity','strategyEvenTrades','strategyGrossLoss','strategyGrossLossPercent','strategyGrossProfit','strategyGrossProfitPercent','strategyInitialCapital','strategyLossTrades','strategyMarginLiquidationPrice','strategyMaxContractsHeldAll','strategyMaxContractsHeldLong','strategyMaxContractsHeldShort','strategyMaxDrawdown','strategyMaxDrawdownPercent','strategyMaxRunup','strategyMaxRunupPercent','strategyNetProfit','strategyNetProfitPercent','strategyOpenProfit','strategyOpenProfitPercent','strategyOpenTrades','strategyOpenTradesCapitalHeld','strategyPositionAvgPrice','strategyPositionEntryName','strategyPositionSize','strategyWinTrades','symInfoBaseCurrency','symInfoCountry','symInfoCurrency','symInfoDescription','symInfoEmployees','symInfoExpirationDate','symInfoIndustry','symInfoMainTickerId','symInfoMinContract','symInfoMinMove','symInfoMinTick','symInfoPointValue','symInfoPrefix','symInfoPriceScale','symInfoRecommendationsBuy','symInfoRecommendationsBuyStrong','symInfoRecommendationsDate','symInfoRecommendationsHold','symInfoRecommendationsSell','symInfoRecommendationsSellStrong','symInfoRecommendationsTotal','symInfoRoot','symInfoSector','symInfoSession','symInfoShareholders','symInfoSharesOutstandingFloat','symInfoSharesOutstandingTotal','symInfoTargetPriceAverage','symInfoTargetPriceDate','symInfoTargetPriceEstimates','symInfoTargetPriceHigh','symInfoTargetPriceLow','symInfoTargetPriceMedian','symInfoTicker','symInfoTickerId','symInfoTimezone','symInfoType','symInfoVolumeType','taAccDist','taIII','taNVI','taOBV','taPVI','taPVT','taTR','taVWAP','taWAD','taWVAD','tableAll','time','timeClose','timeTradingDay','timeframeIsDaily','timeframeIsDWM','timeframeIsIntraday','timeframeIsMinutes','timeframeIsMonthly','timeframeIsSeconds','timeframeIsTicks','timeframeIsWeekly','timeframeMainPeriod','timeframeMultiplier','timeframePeriod','timeNow','weekOfYear','year','showStyleArea','showStyleAreaBr','showStyleCircles','showStyleColumns','showStyleCross','showStyleHistogram','showStyleLine','showStyleLineBr','showStyleStepLine','showStyleStepLineDiamond','showStyleStepLineBr','positionBottomCenter','positionBottomLeft','positionBottomRight','positionMiddleCenter','positionMiddleLeft','positionMiddleRight','positionTopCenter','positionTopLeft','positionTopRight','scaleLeft','scaleNone','scaleRight','sessionExtended','sessionRegular','settlementAsCloseInherit','settlementAsCloseOff','settlementAsCloseOn','shapeArrowDown','shapeArrowUp','shapeCircle','shapeCross','shapeDiamond','shapeFlag','shapeLabelDown','shapeLabelUp','shapeSquare','shapeTriangleDown','shapeTriangleUp','shapeXCross','sizeAuto','sizeHuge','sizeLarge','sizeNormal','sizeSmall','sizeTiny','splitsDenominator','splitsNumerator','strategyCash','strategyCommissionCashPerContract','strategyCommissionCashPerOrder','strategyCommissionPercent','strategyDirectionAll','strategyDirectionLong','strategyDirectionShort','strategyFixed','strategyLong','strategyOcaCancel','strategyOcaNone','strategyOcaReduce','strategyPercentOfEquity','strategyShort','textAlignBottom','textAlignCenter','textAlignLeft','textAlignRight','textAlignTop','textWrapAuto','textWrapNone','trueValue','xLocBarIndex','xLocBarTime','yLocAboveBar','yLocBelowBar','yLocPrice','adjustmentDividends','adjustmentNone','adjustmentSplits','alertFreqAll','alertFreqOncePerBar','alertFreqOncePerBarClose','backAdjustmentInherit','backAdjustmentOff','backAdjustmentOn','barMergeGapsOff','barMergeGapsOn','barMergeLookaheadOff','barMergeLookaheadOn','colAqua','colBlack','colBlue','colFuchsia','colGray','colGreen','colLime','colMaroon','colNavy','colOlive','colOrange','colPurple','colRed','colSilver','colTeal','colWhite','colYellow','currencyAUD','currencyBTC','currencyCAD','currencyCHF','currencyETH','currencyEUR','currencyGBP','currencyHKD','currencyINR','currencyJPY','currencyKRW','currencyMYR','currencyNOK','currencyNone','currencyNZD','currencyRUB','currencySEK','currencySGD','currencyTRY','currencyUSD','currencyUSDT','currencyZAR','dayOfWeekFriday','dayOfWeekMonday','dayOfWeekSaturday','dayOfWeekSunday','dayOfWeekThursday','dayOfWeekTuesday','dayOfWeekWednesday','displayAll','displayDataWindow','displayNone','displayPane','displayPriceScale','displayStatusLine','dividendsGross','dividendsNet','earningsActual','earningsEstimate','earningsStandardized','extendBoth','extendLeft','extendNone','extendRight','falseValue','fontFamilyDefault','fontFamilyMonospace','formatInherit','formatMinTick','formatPercent','formatPrice','formatVolume','hlineStyleDashed','hlineStyleDotted','hlineStyleSolid','labelStyleArrowDown','labelStyleArrowUp','labelStyleCircle','labelStyleCross','labelStyleDiamond','labelStyleFlag','labelStyleLabelCenter','labelStyleLabelDown','labelStyleLabelLeft','labelStyleLabelLowerLeft','labelStyleLabelLowerRight','labelStyleLabelRight','labelStyleLabelUp','labelStyleLabelUpperLeft','labelStyleLabelUpperRight','labelStyleNone','labelStyleSquare','labelStyleTextOutline','labelStyleTriangleDown','labelStyleTriangleUp','labelStyleXCross','lineStyleArrowBoth','lineStyleArrowLeft','lineStyleArrowRight','lineStyleDashed','lineStyleDotted','lineStyleSolid','locationAboveBar','locationAbsolute','locationBelowBar','locationBottom','locationTop','mathE','mathPhi','mathPi','mathRPhi','orderAscending','orderDescending', 'onTick', 'onBar','=', '+', '-', '*', '/', '%', '==','!', '!=', '>', '<', '>=', '<=', 'and', 'or', 'not', 'if', 'else', 'for', 'while', 'let', 'arr', 'bool', 'box', 'chartPoint', 'col', 'const', 'float', 'int', 'label',             'dayOfMonth', 'dayOfWeek', 'hour', 'minute', 'month','second', 'time', 'timeClose', 'timeTradingDay', 'timeNow','weekOfYear', 'year', 'sessionIsFirstBar', 'sessionIsFirstBarRegular','sessionIsLastBar', 'sessionIsLastBarRegular', 'sessionIsMarket','sessionIsPostMarket', 'sessionIsPreMarket',             'sma', 'ema', 'rsi', 'minvalue', 'maxvalue', 'taAccDist', 'taIII', 'taNVI', 'taOBV', 'taPVI', 'taPVT', 'taTR', 'taVWAP','taWAD', 'taWVAD', 'taAlma', 'taAtr', 'taBarsSince', 'taBb', 'taBbw', 'taCci','taChange', 'taCmo', 'taCog', 'taCorrelation', 'taCross', 'taCrossover','taCrossunder', 'taCum', 'taDev', 'taDmi', 'taEma', 'taFalling', 'taHighest','taHighestBars', 'taHma', 'taKc', 'taKcw', 'taLinReg', 'taLowest','taLowestBars', 'taMacd', 'taMax', 'taMedian', 'taMfi', 'taMin', 'taMode','taMom', 'taPercentile', 'taPercentRank', 'taPivotHigh', 'taPivotLow','taRange', 'taRising', 'taRma', 'taRoc', 'taRsi', 'taSar', 'taSma', 'taStdev','taStoch', 'taSuperTrend', 'taSwma', 'taTsi', 'taValueWhen', 'taVariance','taVwap', 'taVwma', 'taWma', 'taWpr',             'adjustmentDividends', 'adjustmentNone', 'adjustmentSplits','alertFreqAll', 'alertFreqOncePerBar', 'alertFreqOncePerBarClose','colAqua', 'colBlack', 'colBlue', 'colFuchsia', 'colGray','colGreen', 'colLime', 'colMaroon', 'colNavy', 'colOlive','colOrange', 'colPurple', 'colRed', 'colSilver', 'colTeal','colWhite', 'colYellow',            'symInfoRecommendationsBuy', 'symInfoRecommendationsBuyStrong','symInfoRecommendationsDate', 'symInfoRecommendationsHold','symInfoRecommendationsSell', 'symInfoRecommendationsSellStrong','symInfoRecommendationsTotal', 'symInfoTargetPriceAverage','symInfoTargetPriceDate', 'symInfoTargetPriceEstimates','symInfoTargetPriceHigh', 'symInfoTargetPriceLow','symInfoTargetPriceMedian', 'symInfoTicker', 'symInfoTickerId','symInfoTimezone', 'symInfoType', 'symInfoVolumeType', 'symInfoBaseCurrency', 'symInfoCountry', 'symInfoCurrency','symInfoDescription', 'symInfoEmployees', 'symInfoExpirationDate','symInfoIndustry', 'symInfoMainTickerId', 'symInfoMinContract',   'strategyAccountCurrency', 'strategyAvgLosingTrade','strategyAvgLosingTradePercent', 'strategyAvgTrade','strategyAvgTradePercent', 'strategyAvgWinningTrade','strategyAvgWinningTradePercent', 'strategyClosedTrades','strategyClosedTradesFirstIndex', 'strategyEquity', 'strategyEvenTrades','strategyGrossLoss', 'strategyGrossLossPercent', 'strategyGrossProfit','strategyGrossProfitPercent', 'strategyInitialCapital', 'strategyLossTrades','strategyMarginLiquidationPrice', 'strategyMaxContractsHeldAll','strategyMaxContractsHeldLong', 'strategyMaxContractsHeldShort','strategyMaxDrawdown', 'strategyMaxDrawdownPercent', 'strategyMaxRunup','strategyMaxRunupPercent', 'strategyNetProfit', 'strategyNetProfitPercent','strategyOpenProfit', 'strategyOpenProfitPercent', 'strategyOpenTrades','strategyOpenTradesCapitalHeld', 'strategyPositionAvgPrice','strategyPositionEntryName', 'strategyPositionSize', 'strategyWinTrades','sma', 'ema', 'rsi', 'minvalue', 'maxvalue','alertFunc', 'alertConditionFunc', 'arrAbs', 'arrAvg', 'arrBinarySearch', 'arrBinarySearchLeftmost', 'arrBinarySearchRightmost', 'arrClear', 'arrConcat', 'arrCopy', 'arrCovariance', 'arrEvery', 'arrFill', 'arrFirst', 'arrFrom', 'arrGet', 'arrIncludes', 'arrIndexOf', 'arrInsert', 'arrJoin', 'arrLast', 'arrLastIndexOf', 'arrMax', 'arrMedian', 'arrMin', 'arrMode', 'arrNewBool', 'arrNewBox', 'aryNewCol', 'arrNewFloat', 'arrNewInt', 'arrNewLabel', 'arrNewLine', 'arrNewLineFill', 'arrNewString', 'arrNewTable', 'arrNewType', 'arrPercentileLinearInterpolation', 'arrPercentileNearestRank', 'arrPercentRank', 'arrPop', 'arrPush', 'arrRange', 'arrRemove', 'arrReverse', 'arrSet', 'arrShift', 'arrSize', 'arrSlice', 'arrSome', 'arrSort', 'arrSortIndices', 'arrStandardize', 'arrStdev', 'arrSum', 'arrUnshift', 'arrVariance', 'barColFunc', 'bgColFunc', 'boolFunc', 'boxFunc', 'boxCopyFunc', 'boxDeleteFunc', 'boxGetBottomFunc', 'boxGetLeftFunc', 'boxGetRightFunc', 'boxGetTopFunc', 'boxNewFunc', 'boxSetBgColFunc', 'boxSetBorderColFunc', 'boxSetBorderStyleFunc', 'boxSetBorderWidthFunc', 'boxSetBottomFunc', 'boxSetBottomRightPointFunc', 'boxSetExtendFunc', 'boxSetLeftFunc', 'boxSetLeftTopFunc', 'boxSetRightFunc', 'boxSetRightBottomFunc', 'boxSetTextFunc', 'boxSetTextColFunc', 'boxSetTextFontFamilyFunc', 'boxSetTextHAlignFunc', 'boxSetTextSizeFunc', 'boxSetTextVAlignFunc', 'boxSetTextWrapFunc', 'boxSetTopFunc', 'boxSetTopLeftPointFunc', 'chartPointCopyFunc', 'chartPointFromIndexFunc', 'chartPointFromTimeFunc', 'chartPointNewFunc', 'chartPointNowFunc', 'colFunc', 'colBFunc', 'colFromGradientFunc', 'colGFunc', 'colNewFunc', 'colRFunc', 'colRgbFunc', 'colTFunc', 'dayOfMonthFunc', 'dayOfWeekFunc', 'fillFunc', 'fixNanFunc', 'floatFunc', 'hLineFunc', 'hourFunc', 'indicatorFunc', 'inputFunc', 'inputBoolFunc', 'inputColFunc', 'inputEnumFunc', 'inputFloatFunc', 'inputIntFunc', 'inputPriceFunc', 'inputSessionFunc', 'inputSourceFunc', 'inputStringFunc', 'inputSymbolFunc', 'inputTextAreaFunc', 'inputTimeFunc', 'inputTimeFrameFunc', 'intFunc', 'labelFunc', 'labelCopyFunc', 'labelDeleteFunc', 'labelGetTextFunc', 'labelGetXFunc', 'labelGetYFunc', 'labelNewFunc', 'labelSetColFunc', 'labelSetPointFunc', 'labelSetSizeFunc', 'labelSetStyleFunc', 'labelSetTextFunc', 'labelSetTextFontFamilyFunc', 'labelSetTextAlignFunc', 'labelSetTextColFunc', 'labelSetToolTipFunc', 'labelSetXFunc', 'labelSetXLocFunc', 'labelSetXYFunc', 'labelSetYFunc', 'labelSetYLocFunc', 'libraryFunc', 'lineFunc', 'lineCopyFunc', 'lineDeleteFunc', 'lineGetPriceFunc', 'lineGetX1Func', 'lineGetX2Func', 'lineGetY1Func', 'lineGetY2Func', 'lineNewFunc', 'lineSetColFunc', 'lineSetExtendFunc', 'lineSetFirstPointFunc', 'lineSetSecondPointFunc', 'lineSetStyleFunc', 'lineSetWidthFunc', 'lineSetX1Func', 'lineSetX2Func', 'lineSetXLocFunc', 'lineSetXY1Func', 'lineSetXY2Func', 'lineSetY1Func', 'lineSetY2Func', 'lineFillFunc', 'lineFillDeleteFunc', 'lineFillGetLine1Func', 'lineFillGetLine2Func', 'lineFillNewFunc', 'lineFillSetColFunc', 'logErrorFunc', 'logInfoFunc', 'logWarningFunc', 'mapClearFunc', 'mapContainsFunc', 'mapCopyFunc', 'mapGetFunc', 'mapKeysFunc', 'mapNewTypeFunc', 'mapPutFunc', 'mapPutAllFunc', 'mapRemoveFunc', 'mapSizeFunc', 'mapValuesFunc', 'mathAbsFunc', 'mathAcosFunc', 'mathAsinFunc', 'mathAtanFunc', 'mathAvgFunc', 'mathCeilFunc', 'mathCosFunc', 'mathExpFunc', 'mathFloorFunc', 'mathLogFunc', 'mathLog10Func', 'mathMaxFunc', 'mathMinFunc', 'mathPowFunc', 'mathRandomFunc', 'mathRoundFunc', 'mathRoundToMinTickFunc', 'mathSignFunc', 'mathSinFunc', 'mathSqrtFunc', 'mathSumFunc', 'mathTanFunc', 'mathToDegreesFunc', 'mathToRadiansFunc', 'matrixAddColFunc', 'matrixAddRowFunc', 'matrixAvgFunc', 'matrixColFunc', 'matrixColumnsFunc', 'matrixConcatFunc', 'matrixCopyFunc', 'matrixDetFunc', 'matrixDiffFunc', 'matrixEigenValuesFunc', 'matrixEigenVectorsFunc', 'matrixElementsCountFunc', 'matrixFillFunc', 'matrixGetFunc', 'matrixInvFunc', 'matrixIsAntiDiagonalFunc', 'matrixIsAntiSymmetricFunc', 'matrixIsBinaryFunc', 'matrixIsDiagonalFunc', 'matrixIsIdentityFunc', 'matrixIsSquareFunc', 'matrixIsStochasticFunc', 'matrixIsSymmetricFunc', 'matrixIsTriangularFunc', 'matrixIsZeroFunc', 'matrixKronFunc', 'matrixMaxFunc', 'matrixMedianFunc', 'matrixMinFunc', 'matrixModeFunc', 'matrixMultFunc', 'matrixNewTypeFunc', 'matrixPinvFunc', 'matrixPowFunc', 'matrixRankFunc', 'matrixRemoveColFunc', 'matrixRemoveRowFunc', 'matrixReshapeFunc', 'matrixReverseFunc', 'matrixRowFunc', 'matrixRowsFunc', 'matrixSetFunc', 'matrixSortFunc', 'matrixSubMatrixFunc', 'matrixSumFunc', 'matrixSwapColumnsFunc', 'matrixSwapRowsFunc', 'matrixTraceFunc', 'matrixTransposeFunc', 'maxBarsBackFunc', 'minuteFunc', 'monthFunc', 'naFunc', 'nzFunc', 'polylineDeleteFunc', 'polylineNewFunc', 'requestCurrencyRateFunc', 'requestDividendsFunc', 'requestEarningsFunc', 'requestEconomicFunc', 'requestFinancialFunc', 'requestQuandlFunc', 'requestSecurityFunc', 'requestSecurityLowerTfFunc', 'requestSeedFunc', 'requestSplitsFunc', 'runtimeErrorFunc', 'secondFunc', 'strContainsFunc', 'strEndsWithFunc', 'strFormatFunc', 'strFormatTimeFunc', 'strLengthFunc', 'strLowerFunc', 'strMatchFunc', 'strPosFunc', 'strRepeatFunc', 'strReplaceFunc', 'strReplaceAllFunc', 'strSplitFunc', 'strStartsWithFunc', 'strSubstringFunc', 'strToNumberFunc', 'strToStringFunc', 'strTrimFunc', 'strUpperFunc', 'strategyFunc', 'strategyCancelFunc', 'strategyCancelAllFunc', 'strategyCloseFunc', 'strategyCloseAllFunc', 'strategyClosedTradesCommissionFunc', 'strategyClosedTradesEntryBarIndexFunc', 'strategyClosedTradesEntryCommentFunc', 'strategyClosedTradesEntryIdFunc', 'strategyClosedTradesEntryPriceFunc', 'strategyClosedTradesEntryTimeFunc', 'strategyClosedTradesExitBarIndexFunc', 'strategyClosedTradesExitCommentFunc', 'strategyClosedTradesExitIdFunc', 'strategyClosedTradesExitPriceFunc', 'strategyClosedTradesExitTimeFunc', 'strategyClosedTradesMaxDrawdownFunc', 'strategyClosedTradesMaxDrawdownPercentFunc', 'strategyClosedTradesMaxRunupFunc', 'strategyClosedTradesMaxRunupPercentFunc', 'strategyClosedTradesProfitFunc', 'strategyClosedTradesProfitPercentFunc', 
                                      'strategyClosedTradesSizeFunc', 'strategyConvertToAccountFunc', 'strategyConvertToSymbolFunc', 'strategyDefaultEntryQtyFunc', 'strategyEntryFunc', 'strategyExitFunc', 'strategyOpenTradesCommissionFunc', 'strategyOpenTradesEntryBarIndexFunc', 'strategyOpenTradesEntryCommentFunc', 'strategyOpenTradesEntryIdFunc', 'strategyOpenTradesEntryPriceFunc', 'strategyOpenTradesEntryTimeFunc', 'strategyOpenTradesMaxDrawdownFunc', 'strategyOpenTradesMaxDrawdownPercentFunc', 'strategyOpenTradesMaxRunupFunc', 'strategyOpenTradesMaxRunupPercentFunc', 'strategyOpenTradesProfitFunc', 'strategyOpenTradesProfitPercentFunc', 'strategyOpenTradesSizeFunc', 'strategyOrderFunc', 'strategyRiskAllowEntryInFunc', 'strategyRiskMaxConsLossDaysFunc', 'strategyRiskMaxDrawdownFunc', 'strategyRiskMaxIntradayFilledOrdersFunc', 'strategyRiskMaxIntradayLossFunc', 'strategyRiskMaxPositionSizeFunc', 'symInfoPrefixFunc', 'symInfoTickerFunc', 'timeFunc', 'timeCloseFunc', 'timeframeChangeFunc', 'timeframeFromSecondsFunc', 'timeframeInSecondsFunc', 'timestampFunc', 'weekOfYearFunc', 'yearFunc',             'show', 'showshape', 'showcond','solid', 'dotted', 'dashed','fontFamilyDefault', 'fontFamilyMonospace','extendBoth', 'extendLeft', 'extendNone', 'extendRight','hlineStyleDashed', 'hlineStyleDotted', 'hlineStyleSolid','tableFunc ','tableCellFunc','tableCellSetBgColFunc','tableCellSetHeightFunc' ,'tableCellSetTextFunc','tableCellSetTextColFunc','tableCellSetTextFontFamily','tableCellSetTextHAlignFunc','tableCellSetTextSizeFunc','tableCellSetTextVAlignFunc','tableCellSetToolTipFunc','tableCellSetWidthFunc','tableClearFunc ','tableDeleteFunc ','tableMergeCellsFunc','tableNewFunc','tableSetBgColFunc','tableSetBorderColFunc','tableSetBorderWidthFunc','tableSetFrameColFunc ','tableSetFrameWidthFunc','tableSetPositionFunc',
                                      # Indicator Functions
                                        'adLine', 'adOsc', 'adx', 'adxr', 'apo', 'aroon', 'aroonOsc', 'atr', 'avgPrice', 
                                        'bbands', 'beta', 'bop', 'cci', 'cmo', 'correl', 'dema', 'dx', 'ema', 
                                        'htDcPeriod', 'htDcPhase', 'htPhasor', 'htSine', 'htTrendline', 'htTrendMode',
                                        'kama', 'linearReg', 'linearRegAngle', 'linearRegIntercept', 'linearRegSlope',
                                        'ma', 'macd', 'macdExt', 'macdFix', 'mama', 'maxIndex', 'medPrice', 'mfi',
                                        'midPoint', 'midPrice', 'minIndex', 'minMax', 'minMaxIndex', 'minusDI', 'minusDM',
                                        'mom', 'natr', 'obv', 'plusDI', 'plusDM', 'ppo', 'roc', 'rocp', 'rocr', 'rocr100',
                                        'rsi', 'sar', 'sarExt', 'sma', 'stdDev', 'stoch', 'stochF', 'stochRsi', 'sum',
                                        't3', 'tema', 'tRange', 'trima', 'trix', 'tsf', 'typPrice', 'ultOsc', 'variance',
                                        'wclPrice', 'willr', 'wma',
                                        # Pattern Recognition Functions
                                        'pattern2Crows', 'pattern3BlackCrows', 'pattern3Inside', 'pattern3LineStrike',
                                        'pattern3StarsInSouth', 'pattern3WhiteSoldiers', 'patternAbandonedBaby',
                                        'patternAdvanceBlock', 'patternBeltHold', 'patternBreakaway', 'patternClosingMarubozu',
                                        'patternConcealBabySwallow', 'patternCounterattack', 'patternDarkCloud', 'patternDoji',
                                        'patternDojiStar', 'patternDragonflyDoji', 'patternEngulfing', 'patternEveningDojiStar',
                                        'patternEveningStar', 'patternGapSideSide', 'patternGravestoneDoji', 'patternHammer',
                                        'patternHangingMan', 'patternHarami', 'patternHaramiCross', 'patternHighWave',
                                        'patternHikkake', 'patternHikkakeMod', 'patternHomingPigeon', 'patternIdentical3Crows',
                                        'patternInNeck', 'patternInvertedHammer', 'patternKicking', 'patternKickingByLength',
                                        'patternLadderBottom', 'patternLongLeggedDoji', 'patternLongLine', 'patternMarubozu',
                                        'patternMatchingLow', 'patternMatHold', 'patternMorningDojiStar', 'patternMorningStar',
                                        'patternOnNeck', 'patternPiercing', 'patternRickshawMan', 'patternRiseFall3Methods',
                                        'patternSeparatingLines', 'patternShootingStar', 'patternShortLine', 'patternSpinningTop',
                                        'patternStalledPattern', 'patternStickSandwich', 'patternTakuri', 'patternTasukiGap',
                                        'patternThrusting', 'patternTristar', 'patternUnique3River', 'patternUpsideGap2Crows',
                                        'patternXsideGap3Methods']:
                        tokens.append(('SYNTAX', identifier))
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
    


class DevScriptAutocomplete:
    def __init__(self, registry):
        self.registry = registry
        self.suggestions = {}
        self._build_suggestions()

    def _build_suggestions(self):
        for func_name, func_info in self.registry['syntax_registry']['elements'].items():
            self.suggestions[func_name] = {
                'type': func_info.get('type'),
                'params': func_info.get('params', {}),
                'description': func_info.get('description', '')
            }

    def get_suggestions(self, prefix):
        return {k: v for k, v in self.suggestions.items() if k.startswith(prefix)}

    def get_signature(self, func_name):
        if func_name in self.suggestions:
            func_info = self.suggestions[func_name]
            params = func_info.get('params', {})
            param_str = ', '.join([f"{name}: {p['type']}" for name, p in params.items()])
            return f"{func_name}({param_str})"

    def get_param_suggestions(self, func_name, param_name):
        if func_name in self.suggestions:
            params = self.suggestions[func_name].get('params', {})
            if param_name in params:
                param_type = params[param_name]['type']
                return self._get_type_suggestions(param_type)

    def _get_type_suggestions(self, param_type):
        type_suggestions = {
            'series': ['close', 'open', 'high', 'low', 'hl2', 'hlc3', 'ohlc4', 'volume'],
            'integer': range(1, 501),
            'color': ['color.red', 'color.green', 'color.blue'],
            'string': [],
            'bool': ['true', 'false']
        }
        return type_suggestions.get(param_type, [])





class DevScriptInterpreter:
    def __init__(self):
        self.registry = self._initialize_registries()
        self.autocomplete = DevScriptAutocomplete(self.registry)
        
    def suggest_completion(self, current_text, cursor_position):
        # Get the word being typed
        word = self._get_current_word(current_text, cursor_position)
        suggestions = self.autocomplete.get_suggestions(word)
        
        # Handle function parameters
        if '(' in current_text:
            func_name = current_text.split('(')[0].strip()
            param_position = self._get_param_position(current_text, cursor_position)
            if param_position is not None:
                return self.autocomplete.get_param_suggestions(func_name, param_position)
                
        return suggestions

    def _get_current_word(self, text, position):
        left = text.rfind(' ', 0, position)
        right = text.find(' ', position)
        return text[left+1:right] if right != -1 else text[left+1:]
        
    def _get_param_position(self, text, position):
        func_text = text[:position]
        params = func_text.split('(')[1].split(',')
        return len(params) - 1


"""-----------------------------------------------------------------------------------------------------------------------------------------"""

# Parser

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        # Using the syntax list directly from Tokenizer's identifier_syntax
        self.syntax_list = ['open', 'high', 'low', 'close', 'volume', 'hl2', 'hlc3', 'hlcc4', 'ohlc4','symInfoMinMove', 'symInfoMinTick',
                             'symInfoPointValue', 'symInfoPrefix','symInfoPriceScale', 'symInfoRoot', 'symInfoSector', 'symInfoSession','symInfoShareholders', 'symInfoSharesOutstandingFloat','symInfoSharesOutstandingTotal',             'sma', 'ema', 'rsi', 'minvalue', 'maxvalue', 'taAccDist', 'taIII', 'taNVI', 'taOBV', 'taPVI', 'taPVT', 'taTR', 'taVWAP','taWAD', 'taWVAD', 'taAlma', 'taAtr', 'taBarsSince', 'taBb', 'taBbw', 'taCci','taChange', 'taCmo', 'taCog', 'taCorrelation', 'taCross', 'taCrossover','taCrossunder', 'taCum', 'taDev', 'taDmi', 'taEma', 'taFalling', 'taHighest','taHighestBars', 'taHma', 'taKc', 'taKcw', 'taLinReg', 'taLowest','taLowestBars', 'taMacd', 'taMax', 'taMedian', 'taMfi', 'taMin', 'taMode','taMom', 'taPercentile', 'taPercentRank', 'taPivotHigh', 'taPivotLow','taRange', 'taRising', 'taRma', 'taRoc', 'taRsi', 'taSar', 'taSma', 'taStdev','taStoch', 'taSuperTrend', 'taSwma', 'taTsi', 'taValueWhen', 'taVariance','taVwap', 'taVwma', 'taWma', 'taWpr', 'strategyAccountCurrency', 'strategyAvgLosingTrade','strategyAvgLosingTradePercent', 'strategyAvgTrade','strategyAvgTradePercent', 'strategyAvgWinningTrade','strategyAvgWinningTradePercent', 'strategyClosedTrades','strategyClosedTradesFirstIndex', 'strategyEquity', 'strategyEvenTrades','strategyGrossLoss', 'strategyGrossLossPercent', 'strategyGrossProfit','strategyGrossProfitPercent', 'strategyInitialCapital', 'strategyLossTrades','strategyMarginLiquidationPrice', 'strategyMaxContractsHeldAll','strategyMaxContractsHeldLong', 'strategyMaxContractsHeldShort','strategyMaxDrawdown', 'strategyMaxDrawdownPercent', 'strategyMaxRunup','strategyMaxRunupPercent', 'strategyNetProfit', 'strategyNetProfitPercent','strategyOpenProfit', 'strategyOpenProfitPercent', 'strategyOpenTrades','strategyOpenTradesCapitalHeld', 'strategyPositionAvgPrice','strategyPositionEntryName', 'strategyPositionSize', 'strategyWinTrades',             'dayOfMonth', 'dayOfWeek', 'hour', 'minute', 'month','second', 'time', 'timeClose', 'timeTradingDay', 'timeNow','weekOfYear', 'year', 'sessionIsFirstBar', 'sessionIsFirstBarRegular','sessionIsLastBar', 'sessionIsLastBarRegular', 'sessionIsMarket','sessionIsPostMarket', 'sessionIsPreMarket',             'boxAll', 'chartBgCol', 'chartFgCol', 'chartIsHeikinAshi','chartIsKagi', 'chartIsLineBreak', 'chartIsPnf', 'chartIsRange','chartIsRenko', 'chartIsStandard', 'chartLeftVisibleBarTime','chartRightVisibleBarTime', 'labelAll', 'lineAll', 'lineFillAll','polylineAll', 'tableAll', 'andOp', 'enumType', 'exportFunc', 'forLoop', 'forInLoop', 'ifCond', 'importFunc', 'methodFunc', 'notOp', 'orOp', 'switchCase', 'typeDef', 'let', 'letip', 'whileLoop','open','high','low','close','volume','barIndex','barStateIsConfirmed','barStateIsFirst','barStateIsHistory','barStateIsLast','barStateIsLastConfirmedHistory','barStateIsNew','barStateIsRealtime','boxAll','chartBgCol','chartFgCol','chartIsHeikinAshi','chartIsKagi','chartIsLineBreak','chartIsPnf','chartIsRange','chartIsRenko','chartIsStandard','chartLeftVisibleBarTime','chartRightVisibleBarTime','dayOfMonth','dayOfWeek','dividendsFutureAmount','dividendsFutureExDate','dividendsFuturePayDate','earningsFutureEps','earningsFuturePeriodEndTime','earningsFutureRevenue','earningsFutureTime','hl2','hlc3','hlcc4','hour','labelAll','lastBarIndex','lastBarTime','lineAll','lineFillAll','minute','month','na','ohlc4','polylineAll','second','sessionIsFirstBar','sessionIsFirstBarRegular','sessionIsLastBar','sessionIsLastBarRegular','sessionIsMarket','sessionIsPostMarket','sessionIsPreMarket','strategyAccountCurrency','strategyAvgLosingTrade','strategyAvgLosingTradePercent','strategyAvgTrade','strategyAvgTradePercent','strategyAvgWinningTrade','strategyAvgWinningTradePercent','strategyClosedTrades','strategyClosedTradesFirstIndex','strategyEquity','strategyEvenTrades','strategyGrossLoss','strategyGrossLossPercent','strategyGrossProfit','strategyGrossProfitPercent','strategyInitialCapital','strategyLossTrades','strategyMarginLiquidationPrice','strategyMaxContractsHeldAll','strategyMaxContractsHeldLong','strategyMaxContractsHeldShort','strategyMaxDrawdown','strategyMaxDrawdownPercent','strategyMaxRunup','strategyMaxRunupPercent','strategyNetProfit','strategyNetProfitPercent','strategyOpenProfit','strategyOpenProfitPercent','strategyOpenTrades','strategyOpenTradesCapitalHeld','strategyPositionAvgPrice','strategyPositionEntryName','strategyPositionSize','strategyWinTrades','symInfoBaseCurrency','symInfoCountry','symInfoCurrency','symInfoDescription','symInfoEmployees','symInfoExpirationDate','symInfoIndustry','symInfoMainTickerId','symInfoMinContract','symInfoMinMove','symInfoMinTick','symInfoPointValue','symInfoPrefix','symInfoPriceScale','symInfoRecommendationsBuy','symInfoRecommendationsBuyStrong','symInfoRecommendationsDate','symInfoRecommendationsHold','symInfoRecommendationsSell','symInfoRecommendationsSellStrong','symInfoRecommendationsTotal','symInfoRoot','symInfoSector','symInfoSession','symInfoShareholders','symInfoSharesOutstandingFloat','symInfoSharesOutstandingTotal','symInfoTargetPriceAverage','symInfoTargetPriceDate','symInfoTargetPriceEstimates','symInfoTargetPriceHigh','symInfoTargetPriceLow','symInfoTargetPriceMedian','symInfoTicker','symInfoTickerId','symInfoTimezone','symInfoType','symInfoVolumeType','taAccDist','taIII','taNVI','taOBV','taPVI','taPVT','taTR','taVWAP','taWAD','taWVAD','tableAll','time','timeClose','timeTradingDay','timeframeIsDaily','timeframeIsDWM','timeframeIsIntraday','timeframeIsMinutes','timeframeIsMonthly','timeframeIsSeconds','timeframeIsTicks','timeframeIsWeekly','timeframeMainPeriod','timeframeMultiplier','timeframePeriod','timeNow','weekOfYear','year','showStyleArea','showStyleAreaBr','showStyleCircles','showStyleColumns','showStyleCross','showStyleHistogram','showStyleLine','showStyleLineBr','showStyleStepLine','showStyleStepLineDiamond','showStyleStepLineBr','positionBottomCenter','positionBottomLeft','positionBottomRight','positionMiddleCenter','positionMiddleLeft','positionMiddleRight','positionTopCenter','positionTopLeft','positionTopRight','scaleLeft','scaleNone','scaleRight','sessionExtended','sessionRegular','settlementAsCloseInherit','settlementAsCloseOff','settlementAsCloseOn','shapeArrowDown','shapeArrowUp','shapeCircle','shapeCross','shapeDiamond','shapeFlag','shapeLabelDown','shapeLabelUp','shapeSquare','shapeTriangleDown','shapeTriangleUp','shapeXCross','sizeAuto','sizeHuge','sizeLarge','sizeNormal','sizeSmall','sizeTiny','splitsDenominator','splitsNumerator','strategyCash','strategyCommissionCashPerContract','strategyCommissionCashPerOrder','strategyCommissionPercent','strategyDirectionAll','strategyDirectionLong','strategyDirectionShort','strategyFixed','strategyLong','strategyOcaCancel','strategyOcaNone','strategyOcaReduce','strategyPercentOfEquity','strategyShort','textAlignBottom','textAlignCenter','textAlignLeft','textAlignRight','textAlignTop','textWrapAuto','textWrapNone','trueValue','xLocBarIndex','xLocBarTime','yLocAboveBar','yLocBelowBar','yLocPrice','adjustmentDividends','adjustmentNone','adjustmentSplits','alertFreqAll','alertFreqOncePerBar','alertFreqOncePerBarClose','backAdjustmentInherit','backAdjustmentOff','backAdjustmentOn','barMergeGapsOff','barMergeGapsOn','barMergeLookaheadOff','barMergeLookaheadOn','colAqua','colBlack','colBlue','colFuchsia','colGray','colGreen','colLime','colMaroon','colNavy','colOlive','colOrange','colPurple','colRed','colSilver','colTeal','colWhite','colYellow','currencyAUD','currencyBTC','currencyCAD','currencyCHF','currencyETH','currencyEUR','currencyGBP','currencyHKD','currencyINR','currencyJPY','currencyKRW','currencyMYR','currencyNOK','currencyNone','currencyNZD','currencyRUB','currencySEK','currencySGD','currencyTRY','currencyUSD','currencyUSDT','currencyZAR','dayOfWeekFriday','dayOfWeekMonday','dayOfWeekSaturday','dayOfWeekSunday','dayOfWeekThursday','dayOfWeekTuesday','dayOfWeekWednesday','displayAll','displayDataWindow','displayNone','displayPane','displayPriceScale','displayStatusLine','dividendsGross','dividendsNet','earningsActual','earningsEstimate','earningsStandardized','extendBoth','extendLeft','extendNone','extendRight','falseValue','fontFamilyDefault','fontFamilyMonospace','formatInherit','formatMinTick','formatPercent','formatPrice','formatVolume','hlineStyleDashed','hlineStyleDotted','hlineStyleSolid','labelStyleArrowDown','labelStyleArrowUp','labelStyleCircle','labelStyleCross','labelStyleDiamond','labelStyleFlag','labelStyleLabelCenter','labelStyleLabelDown','labelStyleLabelLeft','labelStyleLabelLowerLeft','labelStyleLabelLowerRight','labelStyleLabelRight','labelStyleLabelUp','labelStyleLabelUpperLeft','labelStyleLabelUpperRight','labelStyleNone','labelStyleSquare','labelStyleTextOutline','labelStyleTriangleDown','labelStyleTriangleUp','labelStyleXCross','lineStyleArrowBoth','lineStyleArrowLeft','lineStyleArrowRight','lineStyleDashed','lineStyleDotted','lineStyleSolid','locationAboveBar','locationAbsolute','locationBelowBar','locationBottom','locationTop','mathE','mathPhi','mathPi','mathRPhi','orderAscending','orderDescending', 'onTick', 'onBar','=', '+', '-', '*', '/', '%', '==','!', '!=', '>', '<', '>=', '<=', 'and', 'or', 'not', 'if', 'else', 'for', 'while', 'let', 'arr', 'bool', 'box', 'chartPoint', 'col', 'const', 'float', 'int', 'label',             'dayOfMonth', 'dayOfWeek', 'hour', 'minute', 'month','second', 'time', 'timeClose', 'timeTradingDay', 'timeNow','weekOfYear', 'year', 'sessionIsFirstBar', 'sessionIsFirstBarRegular','sessionIsLastBar', 'sessionIsLastBarRegular', 'sessionIsMarket','sessionIsPostMarket', 'sessionIsPreMarket',             'sma', 'ema', 'rsi', 'minvalue', 'maxvalue', 'taAccDist', 'taIII', 'taNVI', 'taOBV', 'taPVI', 'taPVT', 'taTR', 'taVWAP','taWAD', 'taWVAD', 'taAlma', 'taAtr', 'taBarsSince', 'taBb', 'taBbw', 'taCci','taChange', 'taCmo', 'taCog', 'taCorrelation', 'taCross', 'taCrossover','taCrossunder', 'taCum', 'taDev', 'taDmi', 'taEma', 'taFalling', 'taHighest','taHighestBars', 'taHma', 'taKc', 'taKcw', 'taLinReg', 'taLowest','taLowestBars', 'taMacd', 'taMax', 'taMedian', 'taMfi', 'taMin', 'taMode','taMom', 'taPercentile', 'taPercentRank', 'taPivotHigh', 'taPivotLow','taRange', 'taRising', 'taRma', 'taRoc', 'taRsi', 'taSar', 'taSma', 'taStdev','taStoch', 'taSuperTrend', 'taSwma', 'taTsi', 'taValueWhen', 'taVariance','taVwap', 'taVwma', 'taWma', 'taWpr',             'adjustmentDividends', 'adjustmentNone', 'adjustmentSplits','alertFreqAll', 'alertFreqOncePerBar', 'alertFreqOncePerBarClose','colAqua', 'colBlack', 'colBlue', 'colFuchsia', 'colGray','colGreen', 'colLime', 'colMaroon', 'colNavy', 'colOlive','colOrange', 'colPurple', 'colRed', 'colSilver', 'colTeal','colWhite', 'colYellow',            'symInfoRecommendationsBuy', 'symInfoRecommendationsBuyStrong','symInfoRecommendationsDate', 'symInfoRecommendationsHold','symInfoRecommendationsSell', 'symInfoRecommendationsSellStrong','symInfoRecommendationsTotal', 'symInfoTargetPriceAverage','symInfoTargetPriceDate', 'symInfoTargetPriceEstimates','symInfoTargetPriceHigh', 'symInfoTargetPriceLow','symInfoTargetPriceMedian', 'symInfoTicker', 'symInfoTickerId','symInfoTimezone', 'symInfoType', 'symInfoVolumeType', 'symInfoBaseCurrency', 'symInfoCountry', 'symInfoCurrency','symInfoDescription', 'symInfoEmployees', 'symInfoExpirationDate','symInfoIndustry', 'symInfoMainTickerId', 'symInfoMinContract',   'strategyAccountCurrency', 'strategyAvgLosingTrade','strategyAvgLosingTradePercent', 'strategyAvgTrade','strategyAvgTradePercent', 'strategyAvgWinningTrade','strategyAvgWinningTradePercent', 'strategyClosedTrades','strategyClosedTradesFirstIndex', 'strategyEquity', 'strategyEvenTrades','strategyGrossLoss', 'strategyGrossLossPercent', 'strategyGrossProfit','strategyGrossProfitPercent', 'strategyInitialCapital', 'strategyLossTrades','strategyMarginLiquidationPrice', 'strategyMaxContractsHeldAll','strategyMaxContractsHeldLong', 'strategyMaxContractsHeldShort','strategyMaxDrawdown', 'strategyMaxDrawdownPercent', 'strategyMaxRunup','strategyMaxRunupPercent', 'strategyNetProfit', 'strategyNetProfitPercent','strategyOpenProfit', 'strategyOpenProfitPercent', 'strategyOpenTrades','strategyOpenTradesCapitalHeld', 'strategyPositionAvgPrice','strategyPositionEntryName', 'strategyPositionSize', 'strategyWinTrades','sma', 'ema', 'rsi', 'minvalue', 'maxvalue','alertFunc', 'alertConditionFunc', 'arrAbs', 'arrAvg', 'arrBinarySearch', 'arrBinarySearchLeftmost', 'arrBinarySearchRightmost', 'arrClear', 'arrConcat', 'arrCopy', 'arrCovariance', 'arrEvery', 'arrFill', 'arrFirst', 'arrFrom', 'arrGet', 'arrIncludes', 'arrIndexOf', 'arrInsert', 'arrJoin', 'arrLast', 'arrLastIndexOf', 'arrMax', 'arrMedian', 'arrMin', 'arrMode', 'arrNewBool', 'arrNewBox', 'aryNewCol', 'arrNewFloat', 'arrNewInt', 'arrNewLabel', 'arrNewLine', 'arrNewLineFill', 'arrNewString', 'arrNewTable', 'arrNewType', 'arrPercentileLinearInterpolation', 'arrPercentileNearestRank', 'arrPercentRank', 'arrPop', 'arrPush', 'arrRange', 'arrRemove', 'arrReverse', 'arrSet', 'arrShift', 'arrSize', 'arrSlice', 'arrSome', 'arrSort', 'arrSortIndices', 'arrStandardize', 'arrStdev', 'arrSum', 'arrUnshift', 'arrVariance', 'barColFunc', 'bgColFunc', 'boolFunc', 'boxFunc', 'boxCopyFunc', 'boxDeleteFunc', 'boxGetBottomFunc', 'boxGetLeftFunc', 'boxGetRightFunc', 'boxGetTopFunc', 'boxNewFunc', 'boxSetBgColFunc', 'boxSetBorderColFunc', 'boxSetBorderStyleFunc', 'boxSetBorderWidthFunc', 'boxSetBottomFunc', 'boxSetBottomRightPointFunc', 'boxSetExtendFunc', 'boxSetLeftFunc', 'boxSetLeftTopFunc', 'boxSetRightFunc', 'boxSetRightBottomFunc', 'boxSetTextFunc', 'boxSetTextColFunc', 'boxSetTextFontFamilyFunc', 'boxSetTextHAlignFunc', 'boxSetTextSizeFunc', 'boxSetTextVAlignFunc', 'boxSetTextWrapFunc', 'boxSetTopFunc', 'boxSetTopLeftPointFunc', 'chartPointCopyFunc', 'chartPointFromIndexFunc', 'chartPointFromTimeFunc', 'chartPointNewFunc', 'chartPointNowFunc', 'colFunc', 'colBFunc', 'colFromGradientFunc', 'colGFunc', 'colNewFunc', 'colRFunc', 'colRgbFunc', 'colTFunc', 'dayOfMonthFunc', 'dayOfWeekFunc', 'fillFunc', 'fixNanFunc', 'floatFunc', 'hLineFunc', 'hourFunc', 'indicatorFunc', 'inputFunc', 'inputBoolFunc', 'inputColFunc', 'inputEnumFunc', 'inputFloatFunc', 'inputIntFunc', 'inputPriceFunc', 'inputSessionFunc', 'inputSourceFunc', 'inputStringFunc', 'inputSymbolFunc', 'inputTextAreaFunc', 'inputTimeFunc', 'inputTimeFrameFunc', 'intFunc', 'labelFunc', 'labelCopyFunc', 'labelDeleteFunc', 'labelGetTextFunc', 'labelGetXFunc', 'labelGetYFunc', 'labelNewFunc', 'labelSetColFunc', 'labelSetPointFunc', 'labelSetSizeFunc', 'labelSetStyleFunc', 'labelSetTextFunc', 'labelSetTextFontFamilyFunc', 'labelSetTextAlignFunc', 'labelSetTextColFunc', 'labelSetToolTipFunc', 'labelSetXFunc', 'labelSetXLocFunc', 'labelSetXYFunc', 'labelSetYFunc', 'labelSetYLocFunc', 'libraryFunc', 'lineFunc', 'lineCopyFunc', 'lineDeleteFunc', 'lineGetPriceFunc', 'lineGetX1Func', 'lineGetX2Func', 'lineGetY1Func', 'lineGetY2Func', 'lineNewFunc', 'lineSetColFunc', 'lineSetExtendFunc', 'lineSetFirstPointFunc', 'lineSetSecondPointFunc', 'lineSetStyleFunc', 'lineSetWidthFunc', 'lineSetX1Func', 'lineSetX2Func', 'lineSetXLocFunc', 'lineSetXY1Func', 'lineSetXY2Func', 'lineSetY1Func', 'lineSetY2Func', 'lineFillFunc', 'lineFillDeleteFunc', 'lineFillGetLine1Func', 'lineFillGetLine2Func', 'lineFillNewFunc', 'lineFillSetColFunc', 'logErrorFunc', 'logInfoFunc', 'logWarningFunc', 'mapClearFunc', 'mapContainsFunc', 'mapCopyFunc', 'mapGetFunc', 'mapKeysFunc', 'mapNewTypeFunc', 'mapPutFunc', 'mapPutAllFunc', 'mapRemoveFunc', 'mapSizeFunc', 'mapValuesFunc', 'mathAbsFunc', 'mathAcosFunc', 'mathAsinFunc', 'mathAtanFunc', 'mathAvgFunc', 'mathCeilFunc', 'mathCosFunc', 'mathExpFunc', 'mathFloorFunc', 'mathLogFunc', 'mathLog10Func', 'mathMaxFunc', 'mathMinFunc', 'mathPowFunc', 'mathRandomFunc', 'mathRoundFunc', 'mathRoundToMinTickFunc', 'mathSignFunc', 'mathSinFunc', 'mathSqrtFunc', 'mathSumFunc', 'mathTanFunc', 'mathToDegreesFunc', 'mathToRadiansFunc', 'matrixAddColFunc', 'matrixAddRowFunc', 'matrixAvgFunc', 'matrixColFunc', 'matrixColumnsFunc', 'matrixConcatFunc', 'matrixCopyFunc', 'matrixDetFunc', 'matrixDiffFunc', 'matrixEigenValuesFunc', 'matrixEigenVectorsFunc', 'matrixElementsCountFunc', 'matrixFillFunc', 'matrixGetFunc', 'matrixInvFunc', 'matrixIsAntiDiagonalFunc', 'matrixIsAntiSymmetricFunc', 'matrixIsBinaryFunc', 'matrixIsDiagonalFunc', 'matrixIsIdentityFunc', 'matrixIsSquareFunc', 'matrixIsStochasticFunc', 'matrixIsSymmetricFunc', 'matrixIsTriangularFunc', 'matrixIsZeroFunc', 'matrixKronFunc', 'matrixMaxFunc', 'matrixMedianFunc', 'matrixMinFunc', 'matrixModeFunc', 'matrixMultFunc', 'matrixNewTypeFunc', 'matrixPinvFunc', 'matrixPowFunc', 'matrixRankFunc', 'matrixRemoveColFunc', 'matrixRemoveRowFunc', 'matrixReshapeFunc', 'matrixReverseFunc', 'matrixRowFunc', 'matrixRowsFunc', 'matrixSetFunc', 'matrixSortFunc', 'matrixSubMatrixFunc', 'matrixSumFunc', 'matrixSwapColumnsFunc', 'matrixSwapRowsFunc', 'matrixTraceFunc', 'matrixTransposeFunc', 'maxBarsBackFunc', 'minuteFunc', 'monthFunc', 'naFunc', 'nzFunc', 'polylineDeleteFunc', 'polylineNewFunc', 'requestCurrencyRateFunc', 'requestDividendsFunc', 'requestEarningsFunc', 'requestEconomicFunc', 'requestFinancialFunc', 'requestQuandlFunc', 'requestSecurityFunc', 'requestSecurityLowerTfFunc', 'requestSeedFunc', 'requestSplitsFunc', 'runtimeErrorFunc', 'secondFunc', 'strContainsFunc', 'strEndsWithFunc', 'strFormatFunc', 'strFormatTimeFunc', 'strLengthFunc', 'strLowerFunc', 'strMatchFunc', 'strPosFunc', 'strRepeatFunc', 'strReplaceFunc', 'strReplaceAllFunc', 'strSplitFunc', 'strStartsWithFunc', 'strSubstringFunc', 'strToNumberFunc', 'strToStringFunc', 'strTrimFunc', 'strUpperFunc', 'strategyFunc', 'strategyCancelFunc', 'strategyCancelAllFunc', 'strategyCloseFunc', 'strategyCloseAllFunc', 'strategyClosedTradesCommissionFunc', 'strategyClosedTradesEntryBarIndexFunc', 'strategyClosedTradesEntryCommentFunc', 'strategyClosedTradesEntryIdFunc', 'strategyClosedTradesEntryPriceFunc', 'strategyClosedTradesEntryTimeFunc', 'strategyClosedTradesExitBarIndexFunc', 'strategyClosedTradesExitCommentFunc', 'strategyClosedTradesExitIdFunc', 'strategyClosedTradesExitPriceFunc', 'strategyClosedTradesExitTimeFunc', 'strategyClosedTradesMaxDrawdownFunc', 'strategyClosedTradesMaxDrawdownPercentFunc', 'strategyClosedTradesMaxRunupFunc', 'strategyClosedTradesMaxRunupPercentFunc', 'strategyClosedTradesProfitFunc', 'strategyClosedTradesProfitPercentFunc', 'strategyClosedTradesSizeFunc', 'strategyConvertToAccountFunc', 'strategyConvertToSymbolFunc', 'strategyDefaultEntryQtyFunc', 'strategyEntryFunc', 'strategyExitFunc', 'strategyOpenTradesCommissionFunc', 'strategyOpenTradesEntryBarIndexFunc', 'strategyOpenTradesEntryCommentFunc', 'strategyOpenTradesEntryIdFunc', 'strategyOpenTradesEntryPriceFunc', 'strategyOpenTradesEntryTimeFunc', 'strategyOpenTradesMaxDrawdownFunc', 'strategyOpenTradesMaxDrawdownPercentFunc', 'strategyOpenTradesMaxRunupFunc', 'strategyOpenTradesMaxRunupPercentFunc', 'strategyOpenTradesProfitFunc', 'strategyOpenTradesProfitPercentFunc', 'strategyOpenTradesSizeFunc', 'strategyOrderFunc', 'strategyRiskAllowEntryInFunc', 'strategyRiskMaxConsLossDaysFunc', 'strategyRiskMaxDrawdownFunc', 'strategyRiskMaxIntradayFilledOrdersFunc', 'strategyRiskMaxIntradayLossFunc', 'strategyRiskMaxPositionSizeFunc', 'symInfoPrefixFunc', 'symInfoTickerFunc', 'timeFunc', 'timeCloseFunc', 'timeframeChangeFunc', 'timeframeFromSecondsFunc', 'timeframeInSecondsFunc', 'timestampFunc', 'weekOfYearFunc', 'yearFunc',             'show', 'showshape', 'showcond','solid', 'dotted', 'dashed','fontFamilyDefault', 'fontFamilyMonospace','extendBoth', 'extendLeft',
                             'extendNone', 'extendRight','hlineStyleDashed', 'hlineStyleDotted', 'hlineStyleSolid', 'tableFunc ','tableCellFunc','tableCellSetBgColFunc','tableCellSetHeightFunc' ,'tableCellSetTextFunc','tableCellSetTextColFunc','tableCellSetTextFontFamily','tableCellSetTextHAlignFunc','tableCellSetTextSizeFunc','tableCellSetTextVAlignFunc','tableCellSetToolTipFunc','tableCellSetWidthFunc','tableClearFunc ','tableDeleteFunc ','tableMergeCellsFunc','tableNewFunc','tableSetBgColFunc','tableSetBorderColFunc','tableSetBorderWidthFunc','tableSetFrameColFunc ','tableSetFrameWidthFunc','tableSetPositionFunc',
                             # Indicator Functions
                     'adLine', 'adOsc', 'adx', 'adxr', 'apo', 'aroon', 'aroonOsc', 'atr', 'avgPrice', 
                     'bbands', 'beta', 'bop', 'cci', 'cmo', 'correl', 'dema', 'dx', 'ema', 
                     'htDcPeriod', 'htDcPhase', 'htPhasor', 'htSine', 'htTrendline', 'htTrendMode',
                     'kama', 'linearReg', 'linearRegAngle', 'linearRegIntercept', 'linearRegSlope',
                     'ma', 'macd', 'macdExt', 'macdFix', 'mama', 'maxIndex', 'medPrice', 'mfi',
                     'midPoint', 'midPrice', 'minIndex', 'minMax', 'minMaxIndex', 'minusDI', 'minusDM',
                     'mom', 'natr', 'obv', 'plusDI', 'plusDM', 'ppo', 'roc', 'rocp', 'rocr', 'rocr100',
                     'rsi', 'sar', 'sarExt', 'sma', 'stdDev', 'stoch', 'stochF', 'stochRsi', 'sum',
                     't3', 'tema', 'tRange', 'trima', 'trix', 'tsf', 'typPrice', 'ultOsc', 'variance',
                     'wclPrice', 'willr', 'wma',
                     # Pattern Recognition Functions
                     'pattern2Crows', 'pattern3BlackCrows', 'pattern3Inside', 'pattern3LineStrike',
                     'pattern3StarsInSouth', 'pattern3WhiteSoldiers', 'patternAbandonedBaby',
                     'patternAdvanceBlock', 'patternBeltHold', 'patternBreakaway', 'patternClosingMarubozu',
                     'patternConcealBabySwallow', 'patternCounterattack', 'patternDarkCloud', 'patternDoji',
                     'patternDojiStar', 'patternDragonflyDoji', 'patternEngulfing', 'patternEveningDojiStar',
                     'patternEveningStar', 'patternGapSideSide', 'patternGravestoneDoji', 'patternHammer',
                     'patternHangingMan', 'patternHarami', 'patternHaramiCross', 'patternHighWave',
                     'patternHikkake', 'patternHikkakeMod', 'patternHomingPigeon', 'patternIdentical3Crows',
                     'patternInNeck', 'patternInvertedHammer', 'patternKicking', 'patternKickingByLength',
                     'patternLadderBottom', 'patternLongLeggedDoji', 'patternLongLine', 'patternMarubozu',
                     'patternMatchingLow', 'patternMatHold', 'patternMorningDojiStar', 'patternMorningStar',
                     'patternOnNeck', 'patternPiercing', 'patternRickshawMan', 'patternRiseFall3Methods',
                     'patternSeparatingLines', 'patternShootingStar', 'patternShortLine', 'patternSpinningTop',
                     'patternStalledPattern', 'patternStickSandwich', 'patternTakuri', 'patternTasukiGap',
                     'patternThrusting', 'patternTristar', 'patternUnique3River', 'patternUpsideGap2Crows',
                     'patternXsideGap3Methods']

        self.registry = self._initialize_registries()

    def parse_all_syntax(self):
        while self.current_token.type != 'EOF':
            syntax = {
                'name': self.current_token.value,
                'value': self.current_token.value
            }
            if syntax['name'] in self.syntax_list:
                return syntax
            self.current_token = self.lexer.get_next_token()

    def parse_all_syntax(self):
        while self.current_token.type != 'EOF':
            syntax = {
                'name': self.current_token.value,
                'value': self.current_token.value
            }
            if syntax['name'] in self.registry['syntax_registry']['elements']:
                return syntax
            self.current_token = self.lexer.get_next_token()

    def parse(self):
        parsed_syntax = self.parse_all_syntax()
        return self.calculate_syntax(parsed_syntax)


def calculate_syntax(self, syntax_list: dict, *args: Any) -> Union[float, list, dict, None]:
    syntax_info = self.registry['syntax_registry']['elements'].get(syntax_list['name'])
    
    if syntax_info:
        if syntax_list['name'] == 'arrAbs':
            return [abs(x) for x in args[0]]
            
        elif syntax_list['name'] == 'arrAvg':
            return sum(args[0]) / len(args[0])
            
        elif syntax_list['name'] == 'arrBinarySearch':
            left, right = 0, len(args[0]) - 1
            while left <= right:
                mid = (left + right) // 2
                if args[0][mid] == args[1]:
                    return mid
                elif args[0][mid] < args[1]:
                    left = mid + 1
                else:
                    right = mid - 1
            return left
            
        elif syntax_list['name'] == 'arrBinarySearchLeftmost':
            left, right = 0, len(args[0])
            while left < right:
                mid = (left + right) // 2
                if args[0][mid] < args[1]:
                    left = mid + 1
                else:
                    right = mid
            return left
            
        elif syntax_list['name'] == 'arrBinarySearchRightmost':
            left, right = 0, len(args[0])
            while left < right:
                mid = (left + right) // 2
                if args[0][mid] <= args[1]:
                    left = mid + 1
                else:
                    right = mid
            return left
            
        elif syntax_list['name'] == 'arrClear':
            args[0] = []
            return args[0]
            
        elif syntax_list['name'] == 'arrConcat':
            result = []
            for x in args[0]:
                result.append(x)
            for x in args[1]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrCopy':
            result = []
            for x in args[0]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrCovariance':
            mean1 = sum(args[0]) / len(args[0])
            mean2 = sum(args[1]) / len(args[1])
            sum_of_products = sum((x - mean1) * (y - mean2) for x, y in zip(args[0], args[1]))
            return sum_of_products / len(args[0])
            
        elif syntax_list['name'] == 'arrEvery':
            for x in args[0]:
                if not args[1](x):
                    return False
            return True
            
        elif syntax_list['name'] == 'arrFill':
            result = []
            for _ in range(len(args[0])):
                result.append(args[1])
            return result
            
        elif syntax_list['name'] == 'arrFirst':
            if len(args[0]) > 0:
                return args[0][0]
            return None
            
        elif syntax_list['name'] == 'arrFrom':
            result = []
            for x in args[0]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrGet':
            return args[0][args[1]]
            
        elif syntax_list['name'] == 'arrIncludes':
            for x in args[0]:
                if x == args[1]:
                    return True
            return False
            
        elif syntax_list['name'] == 'arrIndexOf':
            for i in range(len(args[0])):
                if args[0][i] == args[1]:
                    return i
            return -1
            
        elif syntax_list['name'] == 'arrInsert':
            result = []
            for i in range(len(args[0])):
                if i == args[1]:
                    result.append(args[2])
                result.append(args[0][i])
            if args[1] >= len(args[0]):
                result.append(args[2])
            return result
            
        elif syntax_list['name'] == 'arrJoin':
            result = str(args[0][0]) if args[0] else ""
            for x in args[0][1:]:
                result += args[1] + str(x)
            return result
            
        elif syntax_list['name'] == 'arrLast':
            if len(args[0]) > 0:
                return args[0][-1]
            return None
            
        elif syntax_list['name'] == 'arrLastIndexOf':
            for i in range(len(args[0])-1, -1, -1):
                if args[0][i] == args[1]:
                    return i
            return -1
            
        elif syntax_list['name'] == 'arrMax':
            if not args[0]:
                return None
            max_val = args[0][0]
            for x in args[0][1:]:
                if x > max_val:
                    max_val = x
            return max_val
            
        elif syntax_list['name'] == 'arrMedian':
            sorted_arr = []
            for x in args[0]:
                sorted_arr.append(x)
            for i in range(len(sorted_arr)):
                for j in range(len(sorted_arr)-1-i):
                    if sorted_arr[j] > sorted_arr[j+1]:
                        sorted_arr[j], sorted_arr[j+1] = sorted_arr[j+1], sorted_arr[j]
            n = len(sorted_arr)
            if n % 2 == 0:
                return (sorted_arr[n//2-1] + sorted_arr[n//2]) / 2
            return sorted_arr[n//2]
            
        elif syntax_list['name'] == 'arrMin':
            if not args[0]:
                return None
            min_val = args[0][0]
            for x in args[0][1:]:
                if x < min_val:
                    min_val = x
            return min_val
            
        elif syntax_list['name'] == 'arrMode':
            if not args[0]:
                return None
            counts = {}
            for x in args[0]:
                if x in counts:
                    counts[x] += 1
                else:
                    counts[x] = 1
            max_count = 0
            mode = None
            for x, count in counts.items():
                if count > max_count:
                    max_count = count
                    mode = x
            return mode
            
        elif syntax_list['name'] == 'arrNewBox':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'aryNewCol':
            result = []
            for _ in range(args[0]):
                result.append([])
            return result
            
        elif syntax_list['name'] == 'arrNewLabel':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewLine':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewLineFill':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewTable':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrNewType':
            result = []
            for _ in range(args[0]):
                result.append(None)
            return result
            
        elif syntax_list['name'] == 'arrPercentileLinearInterpolation':
            sorted_arr = sorted(args[0])
            rank = args[1] * (len(sorted_arr) - 1) / 100
            lower_idx = int(rank)
            fraction = rank - lower_idx
            if lower_idx >= len(sorted_arr) - 1:
                return sorted_arr[-1]
            return sorted_arr[lower_idx] + fraction * (sorted_arr[lower_idx + 1] - sorted_arr[lower_idx])
            
        elif syntax_list['name'] == 'arrPercentileNearestRank':
            sorted_arr = sorted(args[0])
            rank = round(args[1] * (len(sorted_arr) - 1) / 100)
            return sorted_arr[rank]
            
        elif syntax_list['name'] == 'arrRemove':
            result = []
            for x in args[0]:
                if x != args[1]:
                    result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrSome':
            for x in args[0]:
                if args[1](x):
                    return True
            return False
            
        elif syntax_list['name'] == 'arrSortIndices':
            indices = list(range(len(args[0])))
            for i in range(len(indices)):
                for j in range(len(indices)-1-i):
                    if args[0][indices[j]] > args[0][indices[j+1]]:
                        indices[j], indices[j+1] = indices[j+1], indices[j]
            return indices

        elif syntax_list['name'] == 'arrNewBool':
            result = []
            for _ in range(args[0]):
                result.append(False)
            return result
            
        elif syntax_list['name'] == 'arrNewFloat':
            result = []
            for _ in range(args[0]):
                result.append(0.0)
            return result
            
        elif syntax_list['name'] == 'arrNewInt':
            result = []
            for _ in range(args[0]):
                result.append(0)
            return result
            
        elif syntax_list['name'] == 'arrNewString':
            result = []
            for _ in range(args[0]):
                result.append("")
            return result
            
        elif syntax_list['name'] == 'arrPercentRank':
            result = []
            for val in args[0]:
                count = 0
                for x in args[0]:
                    if x < val:
                        count += 1
                result.append(count / len(args[0]))
            return result
            
        elif syntax_list['name'] == 'arrPop':
            if len(args[0]) > 0:
                last_val = args[0][-1]
                args[0] = args[0][:-1]
                return last_val
            return None
            
        elif syntax_list['name'] == 'arrPush':
            args[0].append(args[1])
            return len(args[0])
            
        elif syntax_list['name'] == 'arrRange':
            start = args[0]
            end = args[1]
            step = args[2] if len(args) > 2 else 1
            result = []
            current = start
            while (step > 0 and current < end) or (step < 0 and current > end):
                result.append(current)
                current += step
            return result
            
        elif syntax_list['name'] == 'arrReverse':
            result = []
            for i in range(len(args[0])-1, -1, -1):
                result.append(args[0][i])
            return result
            
        elif syntax_list['name'] == 'arrSet':
            args[0][args[1]] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'arrShift':
            if len(args[0]) > 0:
                first_val = args[0][0]
                args[0] = args[0][1:]
                return first_val
            return None
            
        elif syntax_list['name'] == 'arrSize':
            count = 0
            for _ in args[0]:
                count += 1
            return count
            
        elif syntax_list['name'] == 'arrSlice':
            result = []
            start = args[1]
            end = args[2]
            for i in range(start, end):
                result.append(args[0][i])
            return result
            
        elif syntax_list['name'] == 'arrSort':
            result = args[0].copy()
            for i in range(len(result)):
                for j in range(len(result)-1-i):
                    if result[j] > result[j+1]:
                        result[j], result[j+1] = result[j+1], result[j]
            return result
            
        elif syntax_list['name'] == 'arrStandardize':
            mean = sum(args[0]) / len(args[0])
            squared_diff_sum = sum((x - mean) ** 2 for x in args[0])
            std_dev = (squared_diff_sum / len(args[0])) ** 0.5
            return [(x - mean) / std_dev for x in args[0]]
            
        elif syntax_list['name'] == 'arrStdev':
            mean = sum(args[0]) / len(args[0])
            squared_diff_sum = sum((x - mean) ** 2 for x in args[0])
            return (squared_diff_sum / (len(args[0]) - 1)) ** 0.5
            
        elif syntax_list['name'] == 'arrSum':
            total = 0
            for x in args[0]:
                total += x
            return total
            
        elif syntax_list['name'] == 'arrUnshift':
            result = [args[1]]
            for x in args[0]:
                result.append(x)
            return result
            
        elif syntax_list['name'] == 'arrVariance':
            mean = sum(args[0]) / len(args[0])
            squared_diff_sum = sum((x - mean) ** 2 for x in args[0])
            return squared_diff_sum / (len(args[0]) - 1)




        # ta-lib functions

        elif syntax_list['name'] == 'adLine':
            return talib.AD(args[0], args[1], args[2], args[3])  # high, low, close, volume

        elif syntax_list['name'] == 'adOsc':
            return talib.ADOSC(args[0], args[1], args[2], args[3], fastperiod=args[4], slowperiod=args[5])
        
        elif syntax_list['name'] == 'adx':
            return talib.ADX(args[0], args[1], args[2], timeperiod=args[3])
        
        elif syntax_list['name'] == 'adxr':
            return talib.ADXR(args[0], args[1], args[2], timeperiod=args[3])
        
        elif syntax_list['name'] == 'apo':
            return talib.APO(args[0], fastperiod=args[1], slowperiod=args[2])
        
        elif syntax_list['name'] == 'aroon':
            aroondown, aroonup = talib.AROON(args[0], args[1], timeperiod=args[2])
            return {'down': aroondown, 'up': aroonup}
        
        elif syntax_list['name'] == 'aroonOsc':
            return talib.AROONOSC(args[0], args[1], timeperiod=args[2])
        
        elif syntax_list['name'] == 'atr':
            return talib.ATR(args[0], args[1], args[2], timeperiod=args[3])
        
        elif syntax_list['name'] == 'avgPrice':
            return talib.AVGPRICE(args[0], args[1], args[2], args[3])
        
        elif syntax_list['name'] == 'bbands':
            upper, middle, lower = talib.BBANDS(args[0], timeperiod=args[1], nbdevup=args[2], nbdevdn=args[2])
            return {'upper': upper, 'middle': middle, 'lower': lower}
        
        elif syntax_list['name'] == 'beta':
            return talib.BETA(args[0], args[1], timeperiod=args[2])
        
        elif syntax_list['name'] == 'bop':
            return talib.BOP(args[0], args[1], args[2], args[3])
        
        elif syntax_list['name'] == 'cci':
            return talib.CCI(args[0], args[1], args[2], timeperiod=args[3])
        
        elif syntax_list['name'] == 'cmo':
            return talib.CMO(args[0], timeperiod=args[1])
        
        elif syntax_list['name'] == 'correl':
            return talib.CORREL(args[0], args[1], timeperiod=args[2])
        
        elif syntax_list['name'] == 'dema':
            return talib.DEMA(args[0], timeperiod=args[1])
        
        elif syntax_list['name'] == 'dx':
            return talib.DX(args[0], args[1], args[2], timeperiod=args[3])
        
        elif syntax_list['name'] == 'ema':
            return talib.EMA(args[0], timeperiod=args[1])
        
        elif syntax_list['name'] == 'htDcPeriod':
            return talib.HT_DCPERIOD(args[0])
        
        elif syntax_list['name'] == 'htDcPhase':
            return talib.HT_DCPHASE(args[0])
        
        elif syntax_list['name'] == 'htPhasor':
            inphase, quadrature = talib.HT_PHASOR(args[0])
            return {'inphase': inphase, 'quadrature': quadrature}
        
        elif syntax_list['name'] == 'htSine':
            sine, leadsine = talib.HT_SINE(args[0])
            return {'sine': sine, 'leadsine': leadsine}
        
        elif syntax_list['name'] == 'htTrendline':
            return talib.HT_TRENDLINE(args[0])
        
        elif syntax_list['name'] == 'htTrendMode':
            return talib.HT_TRENDMODE(args[0])

        elif syntax_list['name'] == 'kama':
            return talib.KAMA(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'linearReg':
            return talib.LINEARREG(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'linearRegAngle':
            return talib.LINEARREG_ANGLE(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'linearRegIntercept':
            return talib.LINEARREG_INTERCEPT(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'linearRegSlope':
            return talib.LINEARREG_SLOPE(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'ma':
            return talib.MA(args[0], timeperiod=args[1], matype=args[2])

        elif syntax_list['name'] == 'macd':
            macd, signal, hist = talib.MACD(args[0], fastperiod=args[1], slowperiod=args[2], signalperiod=args[3])
            return {'macd': macd, 'signal': signal, 'hist': hist}

        elif syntax_list['name'] == 'macdExt':
            macd, signal, hist = talib.MACDEXT(args[0], fastperiod=args[1], fastmatype=args[2], slowperiod=args[3], slowmatype=args[4], signalperiod=args[5], signalmatype=args[6])
            return {'macd': macd, 'signal': signal, 'hist': hist}

        elif syntax_list['name'] == 'macdFix':
            macd, signal, hist = talib.MACDFIX(args[0], signalperiod=args[1])
            return {'macd': macd, 'signal': signal, 'hist': hist}

        elif syntax_list['name'] == 'mama':
            mama, fama = talib.MAMA(args[0], fastlimit=args[1], slowlimit=args[2])
            return {'mama': mama, 'fama': fama}

        elif syntax_list['name'] == 'maxIndex':
            return talib.MAXINDEX(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'medPrice':
            return talib.MEDPRICE(args[0], args[1])

        elif syntax_list['name'] == 'mfi':
            return talib.MFI(args[0], args[1], args[2], args[3], timeperiod=args[4])

        elif syntax_list['name'] == 'midPoint':
            return talib.MIDPOINT(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'midPrice':
            return talib.MIDPRICE(args[0], args[1], timeperiod=args[2])

        elif syntax_list['name'] == 'minIndex':
            return talib.MININDEX(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'minMax':
            min_val, max_val = talib.MINMAX(args[0], timeperiod=args[1])
            return {'min': min_val, 'max': max_val}

        elif syntax_list['name'] == 'minMaxIndex':
            minidx, maxidx = talib.MINMAXINDEX(args[0], timeperiod=args[1])
            return {'minidx': minidx, 'maxidx': maxidx}

        elif syntax_list['name'] == 'minusDI':
            return talib.MINUS_DI(args[0], args[1], args[2], timeperiod=args[3])

        elif syntax_list['name'] == 'minusDM':
            return talib.MINUS_DM(args[0], args[1], timeperiod=args[2])

        elif syntax_list['name'] == 'mom':
            return talib.MOM(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'natr':
            return talib.NATR(args[0], args[1], args[2], timeperiod=args[3])

        elif syntax_list['name'] == 'obv':
            return talib.OBV(args[0], args[1])

        elif syntax_list['name'] == 'plusDI':
            return talib.PLUS_DI(args[0], args[1], args[2], timeperiod=args[3])

        elif syntax_list['name'] == 'plusDM':
            return talib.PLUS_DM(args[0], args[1], timeperiod=args[2])

        elif syntax_list['name'] == 'ppo':
            return talib.PPO(args[0], fastperiod=args[1], slowperiod=args[2], matype=args[3])

        elif syntax_list['name'] == 'roc':
            return talib.ROC(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'rocp':
            return talib.ROCP(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'rocr':
            return talib.ROCR(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'rocr100':
            return talib.ROCR100(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'rsi':
            return talib.RSI(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'sar':
            return talib.SAR(args[0], args[1], acceleration=args[2], maximum=args[3])

        elif syntax_list['name'] == 'sarExt':
            return talib.SAREXT(args[0], args[1], startvalue=args[2], offsetonreverse=args[3], accelerationinitlong=args[4], accelerationlong=args[5], accelerationmaxlong=args[6], accelerationinitshort=args[7], accelerationshort=args[8], accelerationmaxshort=args[9])

        elif syntax_list['name'] == 'sma':
            return talib.SMA(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'stdDev':
            return talib.STDDEV(args[0], timeperiod=args[1], nbdev=args[2])

        elif syntax_list['name'] == 'stoch':
            slowk, slowd = talib.STOCH(args[0], args[1], args[2], fastk_period=args[3], slowk_period=args[4], slowk_matype=args[5], slowd_period=args[6], slowd_matype=args[7])
            return {'slowk': slowk, 'slowd': slowd}

        elif syntax_list['name'] == 'stochF':
            fastk, fastd = talib.STOCHF(args[0], args[1], args[2], fastk_period=args[3], fastd_period=args[4], fastd_matype=args[5])
            return {'fastk': fastk, 'fastd': fastd}

        elif syntax_list['name'] == 'stochRsi':
            fastk, fastd = talib.STOCHRSI(args[0], timeperiod=args[1], fastk_period=args[2], fastd_period=args[3], fastd_matype=args[4])
            return {'fastk': fastk, 'fastd': fastd}

        elif syntax_list['name'] == 'sum':
            return talib.SUM(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 't3':
            return talib.T3(args[0], timeperiod=args[1], vfactor=args[2])

        elif syntax_list['name'] == 'tema':
            return talib.TEMA(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'tRange':
            return talib.TRANGE(args[0], args[1], args[2])

        elif syntax_list['name'] == 'trima':
            return talib.TRIMA(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'trix':
            return talib.TRIX(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'tsf':
            return talib.TSF(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'typPrice':
            return talib.TYPPRICE(args[0], args[1], args[2])

        elif syntax_list['name'] == 'ultOsc':
            return talib.ULTOSC(args[0], args[1], args[2], timeperiod1=args[3], timeperiod2=args[4], timeperiod3=args[5])

        elif syntax_list['name'] == 'variance':
            return talib.VAR(args[0], timeperiod=args[1], nbdev=args[2])

        elif syntax_list['name'] == 'wclPrice':
            return talib.WCLPRICE(args[0], args[1], args[2])

        elif syntax_list['name'] == 'willr':
            return talib.WILLR(args[0], args[1], args[2], timeperiod=args[3])

        elif syntax_list['name'] == 'wma':
            return talib.WMA(args[0], timeperiod=args[1])

        elif syntax_list['name'] == 'pattern2Crows':
            return talib.CDL2CROWS(args[0], args[1], args[2], args[3])  # open, high, low, close

        elif syntax_list['name'] == 'pattern3BlackCrows':
            return talib.CDL3BLACKCROWS(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'pattern3Inside':
            return talib.CDL3INSIDE(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'pattern3LineStrike':
            return talib.CDL3LINESTRIKE(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'pattern3StarsInSouth':
            return talib.CDL3STARSINSOUTH(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'pattern3WhiteSoldiers':
            return talib.CDL3WHITESOLDIERS(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternAbandonedBaby':
            return talib.CDLABANDONEDBABY(args[0], args[1], args[2], args[3], penetration=args[4])

        elif syntax_list['name'] == 'patternAdvanceBlock':
            return talib.CDLADVANCEBLOCK(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternBeltHold':
            return talib.CDLBELTHOLD(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternBreakaway':
            return talib.CDLBREAKAWAY(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternClosingMarubozu':
            return talib.CDLCLOSINGMARUBOZU(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternConcealBabySwallow':
            return talib.CDLCONCEALBABYSWALL(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternCounterattack':
            return talib.CDLCOUNTERATTACK(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternDarkCloud':
            return talib.CDLDARKCLOUDCOVER(args[0], args[1], args[2], args[3], penetration=args[4])

        elif syntax_list['name'] == 'patternDoji':
            return talib.CDLDOJI(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternDojiStar':
            return talib.CDLDOJISTAR(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternDragonflyDoji':
            return talib.CDLDRAGONFLYDOJI(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternEngulfing':
            return talib.CDLENGULFING(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternEveningDojiStar':
            return talib.CDLEVENINGDOJISTAR(args[0], args[1], args[2], args[3], penetration=args[4])

        elif syntax_list['name'] == 'patternEveningStar':
            return talib.CDLEVENINGSTAR(args[0], args[1], args[2], args[3], penetration=args[4])

        elif syntax_list['name'] == 'patternGapSideSide':
            return talib.CDLGAPSIDESIDEWHITE(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternGravestoneDoji':
            return talib.CDLGRAVESTONEDOJI(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHammer':
            return talib.CDLHAMMER(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHangingMan':
            return talib.CDLHANGINGMAN(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHarami':
            return talib.CDLHARAMI(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHaramiCross':
            return talib.CDLHARAMICROSS(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHighWave':
            return talib.CDLHIGHWAVE(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHikkake':
            return talib.CDLHIKKAKE(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHikkakeMod':
            return talib.CDLHIKKAKEMOD(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternHomingPigeon':
            return talib.CDLHOMINGPIGEON(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternIdentical3Crows':
            return talib.CDLIDENTICAL3CROWS(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternInNeck':
            return talib.CDLINNECK(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternInvertedHammer':
            return talib.CDLINVERTEDHAMMER(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternKicking':
            return talib.CDLKICKING(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternKickingByLength':
            return talib.CDLKICKINGBYLENGTH(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternLadderBottom':
            return talib.CDLLADDERBOTTOM(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternLongLeggedDoji':
            return talib.CDLLONGLEGGEDDOJI(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternLongLine':
            return talib.CDLLONGLINE(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternMarubozu':
            return talib.CDLMARUBOZU(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternMatchingLow':
            return talib.CDLMATCHINGLOW(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternMatHold':
            return talib.CDLMATHOLD(args[0], args[1], args[2], args[3], penetration=args[4])

        elif syntax_list['name'] == 'patternMorningDojiStar':
            return talib.CDLMORNINGDOJISTAR(args[0], args[1], args[2], args[3], penetration=args[4])

        elif syntax_list['name'] == 'patternMorningStar':
            return talib.CDLMORNINGSTAR(args[0], args[1], args[2], args[3], penetration=args[4])

        elif syntax_list['name'] == 'patternOnNeck':
            return talib.CDLONNECK(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternPiercing':
            return talib.CDLPIERCING(args[0], args[1], args[2], args[3])
        elif syntax_list['name'] == 'patternRickshawMan':
            return talib.CDLRICKSHAWMAN(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternRiseFall3Methods':
            return talib.CDLRISEFALL3METHODS(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternSeparatingLines':
            return talib.CDLSEPARATINGLINES(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternShootingStar':
            return talib.CDLSHOOTINGSTAR(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternShortLine':
            return talib.CDLSHORTLINE(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternSpinningTop':
            return talib.CDLSPINNINGTOP(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternStalledPattern':
            return talib.CDLSTALLEDPATTERN(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternStickSandwich':
            return talib.CDLSTICKSANDWICH(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternTakuri':
            return talib.CDLTAKURI(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternTasukiGap':
            return talib.CDLTASUKIGAP(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternThrusting':
            return talib.CDLTHRUSTING(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternTristar':
            return talib.CDLTRISTAR(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternUnique3River':
            return talib.CDLUNIQUE3RIVER(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternUpsideGap2Crows':
            return talib.CDLUPSIDEGAP2CROWS(args[0], args[1], args[2], args[3])

        elif syntax_list['name'] == 'patternXsideGap3Methods':
            return talib.CDLXSIDEGAP3METHODS(args[0], args[1], args[2], args[3])


        # box
        elif syntax_list['name'] == 'boxFunc':
            return {
                'left': 0,
                'top': 0,
                'right': 0,
                'bottom': 0,
                'text': '',
                'bgColor': '#FFFFFF',
                'borderColor': '#000000',
                'borderWidth': 1,
                'borderStyle': 'solid',
                'textColor': '#000000',
                'textSize': 12,
                'textAlign': 'center',
                'textVAlign': 'middle',
                'textWrap': 'none',
                'textFontFamily': 'Arial'
            }
            
        elif syntax_list['name'] == 'boxCopyFunc':
            return {
                'left': args[0]['left'],
                'top': args[0]['top'],
                'right': args[0]['right'],
                'bottom': args[0]['bottom'],
                'text': args[0]['text'],
                'bgColor': args[0]['bgColor'],
                'borderColor': args[0]['borderColor'],
                'borderWidth': args[0]['borderWidth'],
                'borderStyle': args[0]['borderStyle'],
                'textColor': args[0]['textColor'],
                'textSize': args[0]['textSize'],
                'textAlign': args[0]['textAlign'],
                'textVAlign': args[0]['textVAlign'],
                'textWrap': args[0]['textWrap'],
                'textFontFamily': args[0]['textFontFamily']
            }
            
        elif syntax_list['name'] == 'boxDeleteFunc':
            args[0] = None
            return True
            
        elif syntax_list['name'] == 'boxGetBottomFunc':
            return args[0]['bottom']
            
        elif syntax_list['name'] == 'boxGetLeftFunc':
            return args[0]['left']
            
        elif syntax_list['name'] == 'boxGetRightFunc':
            return args[0]['right']
            
        elif syntax_list['name'] == 'boxGetTopFunc':
            return args[0]['top']
            
        elif syntax_list['name'] == 'boxNewFunc':
            return {
                'left': args[0],
                'top': args[1],
                'right': args[2],
                'bottom': args[3]
            }
            
        elif syntax_list['name'] == 'boxSetBgColFunc':
            args[0]['bgColor'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBorderColFunc':
            args[0]['borderColor'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBorderStyleFunc':
            args[0]['borderStyle'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBorderWidthFunc':
            args[0]['borderWidth'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBottomFunc':
            args[0]['bottom'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetBottomRightPointFunc':
            args[0]['bottom'] = args[1]
            args[0]['right'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetExtendFunc':
            args[0]['extend'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetLeftFunc':
            args[0]['left'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetLeftTopFunc':
            args[0]['left'] = args[1]
            args[0]['top'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetRightFunc':
            args[0]['right'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetRightBottomFunc':
            args[0]['right'] = args[1]
            args[0]['bottom'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextFunc':
            args[0]['text'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextColFunc':
            args[0]['textColor'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextFontFamilyFunc':
            args[0]['textFontFamily'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextHAlignFunc':
            args[0]['textAlign'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextSizeFunc':
            args[0]['textSize'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextVAlignFunc':
            args[0]['textVAlign'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTextWrapFunc':
            args[0]['textWrap'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTopFunc':
            args[0]['top'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'boxSetTopLeftPointFunc':
            args[0]['top'] = args[1]
            args[0]['left'] = args[2]
            return args[0]
 

        #col , day

        elif syntax_list['name'] == 'chartPointCopyFunc':
            return {
                'x': args[0]['x'],
                'y': args[0]['y'],
                'time': args[0]['time'],
                'index': args[0]['index']
            }
            
        elif syntax_list['name'] == 'chartPointFromIndexFunc':
            return {
                'x': args[0],
                'y': 0,
                'time': args[1],
                'index': args[0]
            }
            
        elif syntax_list['name'] == 'chartPointFromTimeFunc':
            return {
                'x': 0,
                'y': 0,
                'time': args[0],
                'index': args[1]
            }
            
        elif syntax_list['name'] == 'chartPointNewFunc':
            return {
                'x': args[0],
                'y': args[1],
                'time': args[2],
                'index': args[3]
            }
            
        elif syntax_list['name'] == 'chartPointNowFunc':
            return {
                'x': args[0],
                'y': args[1],
                'time': args[2],
                'index': 0
            }
            
        elif syntax_list['name'] == 'colFunc':
            return {
                'r': args[0],
                'g': args[1],
                'b': args[2],
                't': args[3] if len(args) > 3 else 255
            }
            
        elif syntax_list['name'] == 'colBFunc':
            return args[0]['b']
            
        elif syntax_list['name'] == 'colFromGradientFunc':
            start_r = args[0]['r']
            start_g = args[0]['g']
            start_b = args[0]['b']
            end_r = args[1]['r']
            end_g = args[1]['g']
            end_b = args[1]['b']
            percent = args[2]
            
            r = start_r + (end_r - start_r) * percent
            g = start_g + (end_g - start_g) * percent
            b = start_b + (end_b - start_b) * percent
            
            return {'r': r, 'g': g, 'b': b, 't': 255}
            
        elif syntax_list['name'] == 'colGFunc':
            return args[0]['g']
            
        elif syntax_list['name'] == 'colNewFunc':
            return {
                'r': args[0],
                'g': args[1],
                'b': args[2],
                't': args[3] if len(args) > 3 else 255
            }
            
        elif syntax_list['name'] == 'colRFunc':
            return args[0]['r']
            
        elif syntax_list['name'] == 'colRgbFunc':
            return {
                'r': (args[0] >> 16) & 255,
                'g': (args[0] >> 8) & 255,
                'b': args[0] & 255,
                't': 255
            }
            
        elif syntax_list['name'] == 'colTFunc':
            return args[0]['t']
            
        elif syntax_list['name'] == 'dayOfMonthFunc':
            return args[0].day
            
        elif syntax_list['name'] == 'dayOfWeekFunc':
            return args[0].weekday()
            
        elif syntax_list['name'] == 'fillFunc':
            return [args[1] for _ in range(args[0])]
            
        elif syntax_list['name'] == 'fixNanFunc':
            return args[1] if args[0] != args[0] else args[0]
            
        elif syntax_list['name'] == 'floatFunc':
            return float(args[0])
            
        elif syntax_list['name'] == 'hLineFunc':
            return {
                'price': args[0],
                'color': args[1] if len(args) > 1 else 'black',
                'width': args[2] if len(args) > 2 else 1,
                'style': args[3] if len(args) > 3 else 'solid'
            }
            
        elif syntax_list['name'] == 'hourFunc':
            return args[0].hour
            
        elif syntax_list['name'] == 'indicatorFunc':
            return {
                'name': args[0],
                'parameters': args[1] if len(args) > 1 else {},
                'series': args[2] if len(args) > 2 else []
            }


        # input
        elif syntax_list['name'] == 'inputFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'input',
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'inputBoolFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'bool',
                'value': True if args[1] else False
            }
            
        elif syntax_list['name'] == 'inputColFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'color',
                'value': {
                    'r': args[1]['r'],
                    'g': args[1]['g'],
                    'b': args[1]['b'],
                    't': args[1]['t']
                }
            }
            
        elif syntax_list['name'] == 'inputEnumFunc':
            return {
                'name': args[0],
                'options': args[1],
                'defval': args[2],
                'type': 'enum',
                'value': args[2]
            }
            
        elif syntax_list['name'] == 'inputFloatFunc':
            return {
                'name': args[0],
                'defval': float(args[1]),
                'minval': float(args[2]) if len(args) > 2 else None,
                'maxval': float(args[3]) if len(args) > 3 else None,
                'step': float(args[4]) if len(args) > 4 else 0.1,
                'type': 'float',
                'value': float(args[1])
            }
            
        elif syntax_list['name'] == 'inputIntFunc':
            return {
                'name': args[0],
                'defval': int(args[1]),
                'minval': int(args[2]) if len(args) > 2 else None,
                'maxval': int(args[3]) if len(args) > 3 else None,
                'type': 'integer',
                'value': int(args[1])
            }
            
        elif syntax_list['name'] == 'inputPriceFunc':
            return {
                'name': args[0],
                'defval': float(args[1]),
                'type': 'price',
                'value': float(args[1])
            }
            
        elif syntax_list['name'] == 'inputSessionFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'session',
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'inputSourceFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'source',
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'inputStringFunc':
            return {
                'name': args[0],
                'defval': str(args[1]),
                'type': 'string',
                'value': str(args[1])
            }
            
        elif syntax_list['name'] == 'inputSymbolFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'symbol',
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'inputTextAreaFunc':
            return {
                'name': args[0],
                'defval': str(args[1]),
                'type': 'textarea',
                'value': str(args[1])
            }
            
        elif syntax_list['name'] == 'inputTimeFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'time',
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'inputTimeFrameFunc':
            return {
                'name': args[0],
                'defval': args[1],
                'type': 'timeframe',
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'intFunc':
            return int(float(args[0]))

        # label , library

        elif syntax_list['name'] == 'labelFunc':
            return {
                'text': '',
                'x': 0,
                'y': 0,
                'color': '#000000',
                'size': 12,
                'style': 'normal',
                'textColor': '#000000',
                'fontFamily': 'Arial',
                'textAlign': 'left',
                'tooltip': '',
                'xLoc': 'bar',
                'yLoc': 'price'
            }
            
        elif syntax_list['name'] == 'labelCopyFunc':
            return {
                'text': args[0]['text'],
                'x': args[0]['x'],
                'y': args[0]['y'],
                'color': args[0]['color'],
                'size': args[0]['size'],
                'style': args[0]['style'],
                'textColor': args[0]['textColor'],
                'fontFamily': args[0]['fontFamily'],
                'textAlign': args[0]['textAlign'],
                'tooltip': args[0]['tooltip'],
                'xLoc': args[0]['xLoc'],
                'yLoc': args[0]['yLoc']
            }
            
        elif syntax_list['name'] == 'labelDeleteFunc':
            args[0] = None
            return True
            
        elif syntax_list['name'] == 'labelGetTextFunc':
            return args[0]['text']
            
        elif syntax_list['name'] == 'labelGetXFunc':
            return args[0]['x']
            
        elif syntax_list['name'] == 'labelGetYFunc':
            return args[0]['y']
            
        elif syntax_list['name'] == 'labelNewFunc':
            return {
                'text': args[0],
                'x': args[1],
                'y': args[2],
                'color': '#000000',
                'size': 12,
                'style': 'normal',
                'textColor': '#000000',
                'fontFamily': 'Arial',
                'textAlign': 'left',
                'tooltip': '',
                'xLoc': 'bar',
                'yLoc': 'price'
            }
            
        elif syntax_list['name'] == 'labelSetColFunc':
            args[0]['color'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetPointFunc':
            args[0]['x'] = args[1]['x']
            args[0]['y'] = args[1]['y']
            return args[0]
            
        elif syntax_list['name'] == 'labelSetSizeFunc':
            args[0]['size'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetStyleFunc':
            args[0]['style'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetTextFunc':
            args[0]['text'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetTextFontFamilyFunc':
            args[0]['fontFamily'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetTextAlignFunc':
            args[0]['textAlign'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetTextColFunc':
            args[0]['textColor'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetToolTipFunc':
            args[0]['tooltip'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetXFunc':
            args[0]['x'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetXLocFunc':
            args[0]['xLoc'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetXYFunc':
            args[0]['x'] = args[1]
            args[0]['y'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetYFunc':
            args[0]['y'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'labelSetYLocFunc':
            args[0]['yLoc'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'libraryFunc':
            return {
                'name': args[0],
                'version': args[1],
                'code': args[2]
            }

        # line
        elif syntax_list['name'] == 'lineFunc':
            return {
                'x1': 0, 'y1': 0,
                'x2': 0, 'y2': 0,
                'color': '#000000',
                'width': 1,
                'style': 'solid',
                'extend': 'none',
                'xLoc': 'bar'
            }
            
        elif syntax_list['name'] == 'lineCopyFunc':
            return {
                'x1': args[0]['x1'],
                'y1': args[0]['y1'],
                'x2': args[0]['x2'],
                'y2': args[0]['y2'],
                'color': args[0]['color'],
                'width': args[0]['width'],
                'style': args[0]['style'],
                'extend': args[0]['extend'],
                'xLoc': args[0]['xLoc']
            }
            
        elif syntax_list['name'] == 'lineDeleteFunc':
            args[0] = None
            return True
            
        elif syntax_list['name'] == 'lineGetPriceFunc':
            return args[0]['y1']
            
        elif syntax_list['name'] == 'lineGetX1Func':
            return args[0]['x1']
            
        elif syntax_list['name'] == 'lineGetX2Func':
            return args[0]['x2']
            
        elif syntax_list['name'] == 'lineGetY1Func':
            return args[0]['y1']
            
        elif syntax_list['name'] == 'lineGetY2Func':
            return args[0]['y2']
            
        elif syntax_list['name'] == 'lineNewFunc':
            return {
                'x1': args[0],
                'y1': args[1],
                'x2': args[2],
                'y2': args[3],
                'color': '#000000',
                'width': 1,
                'style': 'solid',
                'extend': 'none',
                'xLoc': 'bar'
            }
            
        elif syntax_list['name'] == 'lineSetColFunc':
            args[0]['color'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetExtendFunc':
            args[0]['extend'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetFirstPointFunc':
            args[0]['x1'] = args[1]['x']
            args[0]['y1'] = args[1]['y']
            return args[0]
            
        elif syntax_list['name'] == 'lineSetSecondPointFunc':
            args[0]['x2'] = args[1]['x']
            args[0]['y2'] = args[1]['y']
            return args[0]
            
        elif syntax_list['name'] == 'lineSetStyleFunc':
            args[0]['style'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetWidthFunc':
            args[0]['width'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetX1Func':
            args[0]['x1'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetX2Func':
            args[0]['x2'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetXLocFunc':
            args[0]['xLoc'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetXY1Func':
            args[0]['x1'] = args[1]
            args[0]['y1'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetXY2Func':
            args[0]['x2'] = args[1]
            args[0]['y2'] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetY1Func':
            args[0]['y1'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineSetY2Func':
            args[0]['y2'] = args[1]
            return args[0]
            
        elif syntax_list['name'] == 'lineFillFunc':
            return {
                'line1': None,
                'line2': None,
                'color': '#000000'
            }
            
        elif syntax_list['name'] == 'lineFillDeleteFunc':
            args[0] = None
            return True
            
        elif syntax_list['name'] == 'lineFillGetLine1Func':
            return args[0]['line1']
            
        elif syntax_list['name'] == 'lineFillGetLine2Func':
            return args[0]['line2']
            
        elif syntax_list['name'] == 'lineFillNewFunc':
            return {
                'line1': args[0],
                'line2': args[1],
                'color': args[2] if len(args) > 2 else '#000000'
            }
            
        elif syntax_list['name'] == 'lineFillSetColFunc':
            args[0]['color'] = args[1]
            return args[0]

        # map , log

        elif syntax_list['name'] == 'logErrorFunc':
            return {
                'type': 'error',
                'message': args[0],
                'timestamp': args[1]
            }
            
        elif syntax_list['name'] == 'logInfoFunc':
            return {
                'type': 'info',
                'message': args[0],
                'timestamp': args[1]
            }
            
        elif syntax_list['name'] == 'logWarningFunc':
            return {
                'type': 'warning',
                'message': args[0],
                'timestamp': args[1]
            }
            
        elif syntax_list['name'] == 'mapClearFunc':
            args[0].clear()
            return {}
            
        elif syntax_list['name'] == 'mapContainsFunc':
            return args[1] in args[0]
            
        elif syntax_list['name'] == 'mapCopyFunc':
            new_map = {}
            for key in args[0]:
                new_map[key] = args[0][key]
            return new_map
            
        elif syntax_list['name'] == 'mapGetFunc':
            return args[0].get(args[1])
            
        elif syntax_list['name'] == 'mapKeysFunc':
            keys = []
            for key in args[0]:
                keys.append(key)
            return keys
            
        elif syntax_list['name'] == 'mapNewTypeFunc':
            return {}
            
        elif syntax_list['name'] == 'mapPutFunc':
            args[0][args[1]] = args[2]
            return args[0]
            
        elif syntax_list['name'] == 'mapPutAllFunc':
            for key in args[1]:
                args[0][key] = args[1][key]
            return args[0]
            
        elif syntax_list['name'] == 'mapRemoveFunc':
            if args[1] in args[0]:
                del args[0][args[1]]
            return args[0]
            
        elif syntax_list['name'] == 'mapSizeFunc':
            count = 0
            for _ in args[0]:
                count += 1
            return count
            
        elif syntax_list['name'] == 'mapValuesFunc':
            values = []
            for key in args[0]:
                values.append(args[0][key])
            return values


        # math

        elif syntax_list['name'] == 'mathAbsFunc':
            return -args[0] if args[0] < 0 else args[0]
            
        elif syntax_list['name'] == 'mathAcosFunc':
            x = args[0]
            if x < -1 or x > 1:
                return None
            return 3.141592653589793 / 2 - (x + x**3/6 + 3*x**5/40 + 5*x**7/112)
            
        elif syntax_list['name'] == 'mathAsinFunc':
            x = args[0]
            if x < -1 or x > 1:
                return None
            return x + x**3/6 + 3*x**5/40 + 5*x**7/112
            
        elif syntax_list['name'] == 'mathAtanFunc':
            x = args[0]
            return x - x**3/3 + x**5/5 - x**7/7 if abs(x) <= 1 else (3.141592653589793/2 if x > 0 else -3.141592653589793/2)
            
        elif syntax_list['name'] == 'mathAvgFunc':
            sum_val = 0
            count = 0
            for x in args[0]:
                sum_val += x
                count += 1
            return sum_val / count if count > 0 else 0
            
        elif syntax_list['name'] == 'mathCeilFunc':
            integer = int(args[0])
            return integer + 1 if args[0] > integer else integer
            
        elif syntax_list['name'] == 'mathCosFunc':
            x = args[0]
            x = x % (2 * 3.141592653589793)
            return 1 - x**2/2 + x**4/24 - x**6/720
            
        elif syntax_list['name'] == 'mathExpFunc':
            x = args[0]
            result = 1
            term = 1
            for i in range(1, 100):
                term *= x/i
                result += term
                if term < 0.0000001:
                    break
            return result
            
        elif syntax_list['name'] == 'mathFloorFunc':
            integer = int(args[0])
            return integer - 1 if args[0] < integer else integer
            
        elif syntax_list['name'] == 'mathLogFunc':
            x = args[0]
            if x <= 0:
                return None
            y = (x - 1) / (x + 1)
            result = 0
            term = y
            for i in range(1, 100, 2):
                result += term / i
                term *= y * y
                if term < 0.0000001:
                    break
            return 2 * result
            
        elif syntax_list['name'] == 'mathLog10Func':
            x = args[0]
            if x <= 0:
                return None
            return mathLogFunc(x) / 2.302585092994046  # ln(10)
            
        elif syntax_list['name'] == 'mathMaxFunc':
            max_val = args[0][0]
            for x in args[0][1:]:
                if x > max_val:
                    max_val = x
            return max_val
            
        elif syntax_list['name'] == 'mathMinFunc':
            min_val = args[0][0]
            for x in args[0][1:]:
                if x < min_val:
                    min_val = x
            return min_val
            
        elif syntax_list['name'] == 'mathPowFunc':
            result = 1
            for _ in range(int(args[1])):
                result *= args[0]
            return result
            
        elif syntax_list['name'] == 'mathRandomFunc':
            seed = args[0] if args else 1
            a = 1664525
            c = 1013904223
            m = 2**32
            seed = (a * seed + c) % m
            return seed / m
            
        elif syntax_list['name'] == 'mathRoundFunc':
            decimal = args[0] - int(args[0])
            return int(args[0]) + (1 if decimal >= 0.5 else 0)
            
        elif syntax_list['name'] == 'mathRoundToMinTickFunc':
            tick = args[1]
            return round(args[0] / tick) * tick
            
        elif syntax_list['name'] == 'mathSignFunc':
            return 1 if args[0] > 0 else (-1 if args[0] < 0 else 0)
            
        elif syntax_list['name'] == 'mathSinFunc':
            x = args[0]
            x = x % (2 * 3.141592653589793)
            return x - x**3/6 + x**5/120 - x**7/5040
            
        elif syntax_list['name'] == 'mathSqrtFunc':
            x = args[0]
            if x < 0:
                return None
            guess = x / 2
            for _ in range(20):
                new_guess = (guess + x/guess) / 2
                if abs(new_guess - guess) < 0.0000001:
                    break
                guess = new_guess
            return guess
            
        elif syntax_list['name'] == 'mathSumFunc':
            total = 0
            for x in args[0]:
                total += x
            return total
            
        elif syntax_list['name'] == 'mathTanFunc':
            sin_val = mathSinFunc(args[0])
            cos_val = mathCosFunc(args[0])
            return sin_val / cos_val if cos_val != 0 else None
            
        elif syntax_list['name'] == 'mathToDegreesFunc':
            return args[0] * 180 / 3.141592653589793
            
        elif syntax_list['name'] == 'mathToRadiansFunc':
            return args[0] * 3.141592653589793 / 180

        # matrix

        elif syntax_list['name'] == 'matrixAddColFunc':
            result = [row[:] for row in args[0]]
            for i in range(len(result)):
                result[i].append(args[1][i])
            return result
            
        elif syntax_list['name'] == 'matrixAddRowFunc':
            result = [row[:] for row in args[0]]
            result.append(args[1])
            return result
            
        elif syntax_list['name'] == 'matrixAvgFunc':
            sum_val = 0
            count = 0
            for row in args[0]:
                for val in row:
                    sum_val += val
                    count += 1
            return sum_val / count if count > 0 else 0
            
        elif syntax_list['name'] == 'matrixColFunc':
            return [row[args[1]] for row in args[0]]
            
        elif syntax_list['name'] == 'matrixColumnsFunc':
            return len(args[0][0]) if args[0] else 0
            
        elif syntax_list['name'] == 'matrixConcatFunc':
            return [row[:] for row in args[0]] + [row[:] for row in args[1]]
            
        elif syntax_list['name'] == 'matrixCopyFunc':
            return [row[:] for row in args[0]]
            
        elif syntax_list['name'] == 'matrixDetFunc':
            n = len(args[0])
            if n == 1:
                return args[0][0][0]
            if n == 2:
                return args[0][0][0] * args[0][1][1] - args[0][0][1] * args[0][1][0]
            det = 0
            for j in range(n):
                submatrix = [[args[0][i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += ((-1) ** j) * args[0][0][j] * matrixDetFunc(submatrix)
            return det
            
        elif syntax_list['name'] == 'matrixDiffFunc':
            rows = len(args[0])
            cols = len(args[0][0])
            result = [[0] * cols for _ in range(rows)]
            for i in range(rows):
                for j in range(cols):
                    result[i][j] = args[0][i][j] - args[1][i][j]
            return result
            
        elif syntax_list['name'] == 'matrixElementsCountFunc':
            count = 0
            for row in args[0]:
                count += len(row)
            return count
            
        elif syntax_list['name'] == 'matrixFillFunc':
            rows = len(args[0])
            cols = len(args[0][0])
            return [[args[1] for _ in range(cols)] for _ in range(rows)]
            
        elif syntax_list['name'] == 'matrixGetFunc':
            return args[0][args[1]][args[2]]
            
        elif syntax_list['name'] == 'matrixIsAntiDiagonalFunc':
            n = len(args[0])
            for i in range(n):
                for j in range(n):
                    if i + j != n - 1 and args[0][i][j] != 0:
                        return False
            return True
            
        elif syntax_list['name'] == 'matrixIsAntiSymmetricFunc':
            n = len(args[0])
            for i in range(n):
                for j in range(n):
                    if args[0][i][j] != -args[0][j][i]:
                        return False
            return True
            
        elif syntax_list['name'] == 'matrixIsBinaryFunc':
            for row in args[0]:
                for val in row:
                    if val != 0 and val != 1:
                        return False
            return True
            
        elif syntax_list['name'] == 'matrixIsDiagonalFunc':
            n = len(args[0])
            for i in range(n):
                for j in range(n):
                    if i != j and args[0][i][j] != 0:
                        return False
            return True
            
        elif syntax_list['name'] == 'matrixIsIdentityFunc':
            n = len(args[0])
            for i in range(n):
                for j in range(n):
                    if (i == j and args[0][i][j] != 1) or (i != j and args[0][i][j] != 0):
                        return False
            return True
            
        elif syntax_list['name'] == 'matrixIsSquareFunc':
            return len(args[0]) == len(args[0][0])
            
        elif syntax_list['name'] == 'matrixIsStochasticFunc':
            for row in args[0]:
                row_sum = sum(row)
                if abs(row_sum - 1) > 0.000001:
                    return False
            return True
            
        elif syntax_list['name'] == 'matrixIsSymmetricFunc':
            n = len(args[0])
            for i in range(n):
                for j in range(i + 1, n):
                    if args[0][i][j] != args[0][j][i]:
                        return False
            return True
            
        elif syntax_list['name'] == 'matrixIsTriangularFunc':
            n = len(args[0])
            lower = True
            upper = True
            for i in range(n):
                for j in range(n):
                    if i < j and args[0][i][j] != 0:
                        lower = False
                    if i > j and args[0][i][j] != 0:
                        upper = False
            return lower or upper
            
        elif syntax_list['name'] == 'matrixIsZeroFunc':
            for row in args[0]:
                for val in row:
                    if val != 0:
                        return False
            return True
            
        elif syntax_list['name'] == 'matrixMaxFunc':
            max_val = args[0][0][0]
            for row in args[0]:
                for val in row:
                    if val > max_val:
                        max_val = val
            return max_val
            
        elif syntax_list['name'] == 'matrixMinFunc':
            min_val = args[0][0][0]
            for row in args[0]:
                for val in row:
                    if val < min_val:
                        min_val = val
            return min_val
            
        elif syntax_list['name'] == 'matrixMultFunc':
            m1, n1 = len(args[0]), len(args[0][0])
            n2 = len(args[1][0])
            result = [[0] * n2 for _ in range(m1)]
            for i in range(m1):
                for j in range(n2):
                    for k in range(n1):
                        result[i][j] += args[0][i][k] * args[1][k][j]
            return result
            
        elif syntax_list['name'] == 'matrixNewTypeFunc':
            return [[0] * args[1] for _ in range(args[0])]
            
        elif syntax_list['name'] == 'matrixReshapeFunc':
            flat = []
            for row in args[0]:
                flat.extend(row)
            rows, cols = args[1], args[2]
            return [flat[i:i + cols] for i in range(0, len(flat), cols)]
            
        elif syntax_list['name'] == 'matrixReverseFunc':
            return [row[::-1] for row in args[0][::-1]]
            
        elif syntax_list['name'] == 'matrixRowFunc':
            return args[0][args[1]][:]
            
        elif syntax_list['name'] == 'matrixRowsFunc':
            return len(args[0])
            
        elif syntax_list['name'] == 'matrixSetFunc':
            args[0][args[1]][args[2]] = args[3]
            return args[0]
            
        elif syntax_list['name'] == 'matrixSortFunc':
            flat = []
            for row in args[0]:
                flat.extend(row)
            flat.sort()
            rows = len(args[0])
            cols = len(args[0][0])
            return [flat[i:i + cols] for i in range(0, len(flat), cols)]
            
        elif syntax_list['name'] == 'matrixSumFunc':
            total = 0
            for row in args[0]:
                for val in row:
                    total += val
            return total
            
        elif syntax_list['name'] == 'matrixTraceFunc':
            trace = 0
            for i in range(len(args[0])):
                trace += args[0][i][i]
            return trace
            
        elif syntax_list['name'] == 'matrixTransposeFunc':
            rows = len(args[0])
            cols = len(args[0][0])
            return [[args[0][j][i] for j in range(rows)] for i in range(cols)]

        elif syntax_list['name'] == 'matrixEigenValuesFunc':
            n = len(args[0])
            # Power iteration method for dominant eigenvalue
            v = [1] * n
            for _ in range(100):
                # Matrix-vector multiplication
                new_v = [0] * n
                for i in range(n):
                    for j in range(n):
                        new_v[i] += args[0][i][j] * v[j]
                # Normalize
                norm = sum(x*x for x in new_v) ** 0.5
                v = [x/norm for x in new_v]
            # Compute Rayleigh quotient
            eigenvalue = sum(v[i] * sum(args[0][i][j] * v[j] for j in range(n)) for i in range(n))
            return [eigenvalue]
            
        elif syntax_list['name'] == 'matrixEigenVectorsFunc':
            n = len(args[0])
            # Power iteration method for dominant eigenvector
            v = [1] * n
            for _ in range(100):
                new_v = [0] * n
                for i in range(n):
                    for j in range(n):
                        new_v[i] += args[0][i][j] * v[j]
                norm = sum(x*x for x in new_v) ** 0.5
                v = [x/norm for x in new_v]
            return [v]
            
        elif syntax_list['name'] == 'matrixInvFunc':
            n = len(args[0])
            # Augment matrix with identity
            aug = [[args[0][i][j] for j in range(n)] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
            
            # Gaussian elimination
            for i in range(n):
                pivot = aug[i][i]
                for j in range(2*n):
                    aug[i][j] /= pivot
                for k in range(n):
                    if k != i:
                        factor = aug[k][i]
                        for j in range(2*n):
                            aug[k][j] -= factor * aug[i][j]
                            
            return [[aug[i][j+n] for j in range(n)] for i in range(n)]
            
        elif syntax_list['name'] == 'matrixKronFunc':
            m1, n1 = len(args[0]), len(args[0][0])
            m2, n2 = len(args[1]), len(args[1][0])
            result = [[0] * (n1*n2) for _ in range(m1*m2)]
            
            for i in range(m1):
                for j in range(n1):
                    for k in range(m2):
                        for l in range(n2):
                            result[i*m2 + k][j*n2 + l] = args[0][i][j] * args[1][k][l]
            return result
            
        elif syntax_list['name'] == 'matrixPinvFunc':
            # Moore-Penrose pseudoinverse using SVD-like approach
            n = len(args[0])
            m = len(args[0][0])
            
            # Compute A^T * A
            ata = [[sum(args[0][k][i] * args[0][k][j] for k in range(n)) for j in range(m)] for i in range(m)]
            
            # Compute inverse of A^T * A
            inv_ata = matrixInvFunc(ata)
            
            # Compute pseudoinverse
            return [[sum(inv_ata[i][k] * args[0][j][k] for k in range(m)) for j in range(n)] for i in range(m)]
            
        elif syntax_list['name'] == 'matrixPowFunc':
            n = len(args[0])
            power = args[1]
            
            # Initialize result as identity matrix
            result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            
            # Multiply matrix power times
            for _ in range(power):
                new_result = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(n):
                        for k in range(n):
                            new_result[i][j] += result[i][k] * args[0][k][j]
                result = new_result
                
            return result
            
        elif syntax_list['name'] == 'matrixRankFunc':
            # Gaussian elimination to compute rank
            m = [row[:] for row in args[0]]
            rows, cols = len(m), len(m[0])
            rank = 0
            
            for col in range(cols):
                if rank >= rows:
                    break
                    
                # Find pivot
                pivot_row = rank
                while pivot_row < rows and m[pivot_row][col] == 0:
                    pivot_row += 1
                    
                if pivot_row < rows:
                    if pivot_row != rank:
                        m[rank], m[pivot_row] = m[pivot_row], m[rank]
                    
                    # Eliminate column entries
                    for i in range(rank + 1, rows):
                        factor = m[i][col] / m[rank][col]
                        for j in range(col, cols):
                            m[i][j] -= factor * m[rank][j]
                            
                    rank += 1
                    
            return rank

        elif syntax_list['name'] == 'matrixMedianFunc':
            flat = []
            for row in args[0]:
                flat.extend(row)
            flat.sort()
            mid = len(flat) // 2
            return flat[mid] if len(flat) % 2 else (flat[mid-1] + flat[mid]) / 2
            
        elif syntax_list['name'] == 'matrixModeFunc':
            flat = []
            for row in args[0]:
                flat.extend(row)
            counts = {}
            for val in flat:
                counts[val] = counts.get(val, 0) + 1
            max_count = max(counts.values())
            return [k for k, v in counts.items() if v == max_count][0]
            
        elif syntax_list['name'] == 'matrixRemoveColFunc':
            return [[val for j, val in enumerate(row) if j != args[1]] for row in args[0]]
            
        elif syntax_list['name'] == 'matrixRemoveRowFunc':
            return [row for i, row in enumerate(args[0]) if i != args[1]]
            
        elif syntax_list['name'] == 'matrixSubMatrixFunc':
            return [[args[0][i][j] for j in range(args[2], args[4])] 
                    for i in range(args[1], args[3])]
            
        elif syntax_list['name'] == 'matrixSwapColumnsFunc':
            result = [row[:] for row in args[0]]
            for row in result:
                row[args[1]], row[args[2]] = row[args[2]], row[args[1]]
            return result
            
        elif syntax_list['name'] == 'matrixSwapRowsFunc':
            result = [row[:] for row in args[0]]
            result[args[1]], result[args[2]] = result[args[2]], result[args[1]]
            return result


        # request , time

        elif syntax_list['name'] == 'maxBarsBackFunc':
            return {
                'buffer': args[0],
                'max_bars': args[1]
            }
            
        elif syntax_list['name'] == 'minuteFunc':
            return args[0].minute
            
        elif syntax_list['name'] == 'monthFunc':
            return args[0].month
            
        elif syntax_list['name'] == 'naFunc':
            return float('nan')
            
        elif syntax_list['name'] == 'nzFunc':
            return args[1] if args[0] != args[0] else args[0]
            
        elif syntax_list['name'] == 'polylineDeleteFunc':
            args[0] = None
            return True
            
        elif syntax_list['name'] == 'polylineNewFunc':
            return {
                'points': args[0],
                'color': args[1] if len(args) > 1 else '#000000',
                'width': args[2] if len(args) > 2 else 1,
                'style': args[3] if len(args) > 3 else 'solid'
            }
            
        elif syntax_list['name'] == 'requestCurrencyRateFunc':
            return {
                'from_currency': args[0],
                'to_currency': args[1],
                'timestamp': args[2]
            }
            
        elif syntax_list['name'] == 'requestDividendsFunc':
            return {
                'symbol': args[0],
                'from_date': args[1],
                'to_date': args[2]
            }
            
        elif syntax_list['name'] == 'requestEarningsFunc':
            return {
                'symbol': args[0],
                'from_date': args[1],
                'to_date': args[2]
            }
            
        elif syntax_list['name'] == 'requestEconomicFunc':
            return {
                'indicator': args[0],
                'from_date': args[1],
                'to_date': args[2]
            }
            
        elif syntax_list['name'] == 'requestFinancialFunc':
            return {
                'symbol': args[0],
                'statement': args[1],
                'period': args[2]
            }
            
        elif syntax_list['name'] == 'requestQuandlFunc':
            return {
                'code': args[0],
                'from_date': args[1],
                'to_date': args[2]
            }
            
        elif syntax_list['name'] == 'requestSecurityFunc':
            return {
                'symbol': args[0],
                'resolution': args[1],
                'from_date': args[2],
                'to_date': args[3]
            }
            
        elif syntax_list['name'] == 'requestSecurityLowerTfFunc':
            return {
                'symbol': args[0],
                'resolution': args[1],
                'from_date': args[2],
                'to_date': args[3],
                'timeframe': args[4]
            }
            
        elif syntax_list['name'] == 'requestSeedFunc':
            return {
                'seed_value': args[0]
            }
            
        elif syntax_list['name'] == 'requestSplitsFunc':
            return {
                'symbol': args[0],
                'from_date': args[1],
                'to_date': args[2]
            }
            
        elif syntax_list['name'] == 'runtimeErrorFunc':
            return {
                'error_message': args[0],
                'error_type': 'runtime',
                'timestamp': args[1]
            }
            
        elif syntax_list['name'] == 'secondFunc':
            return args[0].second


        # str

        elif syntax_list['name'] == 'strContainsFunc':
            text = args[0]
            search = args[1]
            for i in range(len(text) - len(search) + 1):
                if text[i:i+len(search)] == search:
                    return True
            return False
            
        elif syntax_list['name'] == 'strEndsWithFunc':
            text = args[0]
            search = args[1]
            return text[-len(search):] == search if len(text) >= len(search) else False
            
        elif syntax_list['name'] == 'strFormatFunc':
            text = args[0]
            values = args[1:]
            result = ''
            i = 0
            val_index = 0
            while i < len(text):
                if text[i:i+2] == '{}':
                    result += str(values[val_index])
                    val_index += 1
                    i += 2
                else:
                    result += text[i]
                    i += 1
            return result
            
        elif syntax_list['name'] == 'strFormatTimeFunc':
            timestamp = args[0]
            format_str = args[1]
            dt = args[0]
            return format_str.replace('%Y', str(dt.year))\
                           .replace('%m', str(dt.month).zfill(2))\
                           .replace('%d', str(dt.day).zfill(2))\
                           .replace('%H', str(dt.hour).zfill(2))\
                           .replace('%M', str(dt.minute).zfill(2))\
                           .replace('%S', str(dt.second).zfill(2))
            
        elif syntax_list['name'] == 'strLengthFunc':
            count = 0
            for _ in args[0]:
                count += 1
            return count
            
        elif syntax_list['name'] == 'strLowerFunc':
            result = ''
            for c in args[0]:
                if 'A' <= c <= 'Z':
                    result += chr(ord(c) + 32)
                else:
                    result += c
            return result
            
        elif syntax_list['name'] == 'strMatchFunc':
            text = args[0]
            pattern = args[1]
            return text == pattern
            
        elif syntax_list['name'] == 'strPosFunc':
            text = args[0]
            search = args[1]
            for i in range(len(text) - len(search) + 1):
                if text[i:i+len(search)] == search:
                    return i
            return -1
            
        elif syntax_list['name'] == 'strRepeatFunc':
            result = ''
            for _ in range(args[1]):
                result += args[0]
            return result
            
        elif syntax_list['name'] == 'strReplaceFunc':
            text = args[0]
            old = args[1]
            new = args[2]
            pos = 0
            result = ''
            while pos < len(text):
                if text[pos:pos+len(old)] == old:
                    result += new
                    pos += len(old)
                else:
                    result += text[pos]
                    pos += 1
            return result
            
        elif syntax_list['name'] == 'strReplaceAllFunc':
            text = args[0]
            old = args[1]
            new = args[2]
            result = ''
            i = 0
            while i < len(text):
                if text[i:i+len(old)] == old:
                    result += new
                    i += len(old)
                else:
                    result += text[i]
                    i += 1
            return result
            
        elif syntax_list['name'] == 'strSplitFunc':
            text = args[0]
            delimiter = args[1]
            result = []
            current = ''
            i = 0
            while i < len(text):
                if text[i:i+len(delimiter)] == delimiter:
                    result.append(current)
                    current = ''
                    i += len(delimiter)
                else:
                    current += text[i]
                    i += 1
            result.append(current)
            return result
            
        elif syntax_list['name'] == 'strStartsWithFunc':
            text = args[0]
            search = args[1]
            return text[:len(search)] == search if len(text) >= len(search) else False
            
        elif syntax_list['name'] == 'strSubstringFunc':
            text = args[0]
            start = args[1]
            length = args[2] if len(args) > 2 else len(text) - start
            return text[start:start+length]
            
        elif syntax_list['name'] == 'strToNumberFunc':
            text = args[0].strip()
            result = 0
            decimal = 0
            decimal_pos = 0
            negative = text[0] == '-'
            start = 1 if negative else 0
            
            for i in range(start, len(text)):
                if text[i] == '.':
                    decimal_pos = i
                    continue
                digit = ord(text[i]) - ord('0')
                if decimal_pos:
                    decimal = decimal * 10 + digit
                else:
                    result = result * 10 + digit
                    
            final = result + decimal / (10 ** (len(text) - decimal_pos - 1)) if decimal_pos else result
            return -final if negative else final
            
        elif syntax_list['name'] == 'strToStringFunc':
            return str(args[0])
            
        elif syntax_list['name'] == 'strTrimFunc':
            text = args[0]
            start = 0
            end = len(text)
            while start < end and text[start] in ' \t\n\r':
                start += 1
            while end > start and text[end-1] in ' \t\n\r':
                end -= 1
            return text[start:end]
            
        elif syntax_list['name'] == 'strUpperFunc':
            result = ''
            for c in args[0]:
                if 'a' <= c <= 'z':
                    result += chr(ord(c) - 32)
                else:
                    result += c
            return result
        

        # strategy

        elif syntax_list['name'] == 'strategyFunc':
            return {
                'name': args[0],
                'initial_capital': args[1],
                'currency': args[2],
                'trades': [],
                'open_positions': []
            }
            
        elif syntax_list['name'] == 'strategyCancelFunc':
            return {
                'order_id': args[0],
                'status': 'cancelled'
            }
            
        elif syntax_list['name'] == 'strategyCancelAllFunc':
            return {
                'status': 'all_cancelled'
            }
            
        elif syntax_list['name'] == 'strategyCloseFunc':
            return {
                'position_id': args[0],
                'exit_price': args[1],
                'exit_time': args[2]
            }
            
        elif syntax_list['name'] == 'strategyCloseAllFunc':
            return {
                'exit_price': args[0],
                'exit_time': args[1]
            }
            
        elif syntax_list['name'] == 'strategyClosedTradesCommissionFunc':
            return args[0]['trades'][args[1]]['commission']
            
        elif syntax_list['name'] == 'strategyClosedTradesEntryBarIndexFunc':
            return args[0]['trades'][args[1]]['entry_bar_index']
            
        elif syntax_list['name'] == 'strategyClosedTradesEntryCommentFunc':
            return args[0]['trades'][args[1]]['entry_comment']
            
        elif syntax_list['name'] == 'strategyClosedTradesEntryIdFunc':
            return args[0]['trades'][args[1]]['entry_id']
            
        elif syntax_list['name'] == 'strategyClosedTradesEntryPriceFunc':
            return args[0]['trades'][args[1]]['entry_price']
            
        elif syntax_list['name'] == 'strategyClosedTradesEntryTimeFunc':
            return args[0]['trades'][args[1]]['entry_time']
            
        elif syntax_list['name'] == 'strategyClosedTradesExitBarIndexFunc':
            return args[0]['trades'][args[1]]['exit_bar_index']
            
        elif syntax_list['name'] == 'strategyClosedTradesExitCommentFunc':
            return args[0]['trades'][args[1]]['exit_comment']
            
        elif syntax_list['name'] == 'strategyClosedTradesExitIdFunc':
            return args[0]['trades'][args[1]]['exit_id']
            
        elif syntax_list['name'] == 'strategyClosedTradesExitPriceFunc':
            return args[0]['trades'][args[1]]['exit_price']
            
        elif syntax_list['name'] == 'strategyClosedTradesExitTimeFunc':
            return args[0]['trades'][args[1]]['exit_time']
            
        elif syntax_list['name'] == 'strategyClosedTradesMaxDrawdownFunc':
            return args[0]['trades'][args[1]]['max_drawdown']
            
        elif syntax_list['name'] == 'strategyClosedTradesMaxDrawdownPercentFunc':
            trade = args[0]['trades'][args[1]]
            return (trade['max_drawdown'] / trade['entry_price']) * 100
            
        elif syntax_list['name'] == 'strategyClosedTradesMaxRunupFunc':
            return args[0]['trades'][args[1]]['max_runup']
            
        elif syntax_list['name'] == 'strategyClosedTradesMaxRunupPercentFunc':
            trade = args[0]['trades'][args[1]]
            return (trade['max_runup'] / trade['entry_price']) * 100
            
        elif syntax_list['name'] == 'strategyClosedTradesProfitFunc':
            trade = args[0]['trades'][args[1]]
            return (trade['exit_price'] - trade['entry_price']) * trade['size']
            
        elif syntax_list['name'] == 'strategyClosedTradesProfitPercentFunc':
            trade = args[0]['trades'][args[1]]
            return ((trade['exit_price'] - trade['entry_price']) / trade['entry_price']) * 100
            
        elif syntax_list['name'] == 'strategyClosedTradesSizeFunc':
            return args[0]['trades'][args[1]]['size']
            
        elif syntax_list['name'] == 'strategyConvertToAccountFunc':
            return args[0] * args[1]  # value * exchange_rate
            
        elif syntax_list['name'] == 'strategyConvertToSymbolFunc':
            return args[0] / args[1]  # value / exchange_rate
            
        elif syntax_list['name'] == 'strategyDefaultEntryQtyFunc':
            return {
                'quantity': args[0],
                'status': 'set'
            }
            
        elif syntax_list['name'] == 'strategyEntryFunc':
            return {
                'direction': args[0],
                'size': args[1],
                'price': args[2],
                'comment': args[3]
            }
            
        elif syntax_list['name'] == 'strategyExitFunc':
            return {
                'from_entry': args[0],
                'size': args[1],
                'price': args[2],
                'comment': args[3]
            }
            
        elif syntax_list['name'] == 'strategyOpenTradesCommissionFunc':
            return args[0]['open_positions'][args[1]]['commission']
            
        elif syntax_list['name'] == 'strategyOpenTradesEntryBarIndexFunc':
            return args[0]['open_positions'][args[1]]['entry_bar_index']
            
        elif syntax_list['name'] == 'strategyOpenTradesEntryCommentFunc':
            return args[0]['open_positions'][args[1]]['entry_comment']
            
        elif syntax_list['name'] == 'strategyOpenTradesEntryIdFunc':
            return args[0]['open_positions'][args[1]]['entry_id']
            
        elif syntax_list['name'] == 'strategyOpenTradesEntryPriceFunc':
            return args[0]['open_positions'][args[1]]['entry_price']
            
        elif syntax_list['name'] == 'strategyOpenTradesEntryTimeFunc':
            return args[0]['open_positions'][args[1]]['entry_time']
            
        elif syntax_list['name'] == 'strategyOpenTradesMaxDrawdownFunc':
            return args[0]['open_positions'][args[1]]['max_drawdown']
            
        elif syntax_list['name'] == 'strategyOpenTradesMaxDrawdownPercentFunc':
            pos = args[0]['open_positions'][args[1]]
            return (pos['max_drawdown'] / pos['entry_price']) * 100
            
        elif syntax_list['name'] == 'strategyOpenTradesMaxRunupFunc':
            return args[0]['open_positions'][args[1]]['max_runup']
            
        elif syntax_list['name'] == 'strategyOpenTradesMaxRunupPercentFunc':
            pos = args[0]['open_positions'][args[1]]
            return (pos['max_runup'] / pos['entry_price']) * 100
            
        elif syntax_list['name'] == 'strategyOpenTradesProfitFunc':
            pos = args[0]['open_positions'][args[1]]
            current_price = args[2]
            return (current_price - pos['entry_price']) * pos['size']
            
        elif syntax_list['name'] == 'strategyOpenTradesProfitPercentFunc':
            pos = args[0]['open_positions'][args[1]]
            current_price = args[2]
            return ((current_price - pos['entry_price']) / pos['entry_price']) * 100
            
        elif syntax_list['name'] == 'strategyOpenTradesSizeFunc':
            return args[0]['open_positions'][args[1]]['size']
            
        elif syntax_list['name'] == 'strategyOrderFunc':
            return {
                'type': args[0],
                'direction': args[1],
                'size': args[2],
                'price': args[3],
                'comment': args[4]
            }
            
        elif syntax_list['name'] == 'strategyRiskAllowEntryInFunc':
            return args[0] <= args[1]  # current_risk <= max_risk
            
        elif syntax_list['name'] == 'strategyRiskMaxConsLossDaysFunc':
            return args[0] <= args[1]  # consecutive_loss_days <= max_days
            
        elif syntax_list['name'] == 'strategyRiskMaxDrawdownFunc':
            return args[0] <= args[1]  # current_drawdown <= max_drawdown
            
        elif syntax_list['name'] == 'strategyRiskMaxIntradayFilledOrdersFunc':
            return args[0] <= args[1]  # filled_orders <= max_orders
            
        elif syntax_list['name'] == 'strategyRiskMaxIntradayLossFunc':
            return args[0] <= args[1]  # intraday_loss <= max_loss
            
        elif syntax_list['name'] == 'strategyRiskMaxPositionSizeFunc':
            return args[0] <= args[1]  # position_size <= max_size
        

        # weird functions

        elif syntax_list['name'] == 'symInfoPrefixFunc':
            return args[0].split(':')[0] if ':' in args[0] else ''
            
        elif syntax_list['name'] == 'symInfoTickerFunc':
            return args[0].split(':')[1] if ':' in args[0] else args[0]
            
        elif syntax_list['name'] == 'timeFunc':
            return args[0].timestamp()
            
        elif syntax_list['name'] == 'timeCloseFunc':
            return args[0].replace(hour=16, minute=0, second=0, microsecond=0).timestamp()
            
        elif syntax_list['name'] == 'timeframeChangeFunc':
            return {
                'original': args[0],
                'new': args[1],
                'adjustment': args[2]
            }
            
        elif syntax_list['name'] == 'timeframeFromSecondsFunc':
            seconds = args[0]
            if seconds < 60:
                return f"{seconds}S"
            elif seconds < 3600:
                return f"{seconds//60}M"
            elif seconds < 86400:
                return f"{seconds//3600}H"
            else:
                return f"{seconds//86400}D"
            
        elif syntax_list['name'] == 'timeframeInSecondsFunc':
            timeframe = args[0].upper()
            multiplier = int(''.join(filter(str.isdigit, timeframe)))
            unit = ''.join(filter(str.isalpha, timeframe))
            
            if unit == 'S':
                return multiplier
            elif unit == 'M':
                return multiplier * 60
            elif unit == 'H':
                return multiplier * 3600
            elif unit == 'D':
                return multiplier * 86400
            
        elif syntax_list['name'] == 'timestampFunc':
            return args[0].timestamp()
            
        elif syntax_list['name'] == 'weekOfYearFunc':
            return args[0].isocalendar()[1]
            
        elif syntax_list['name'] == 'yearFunc':
            return args[0].year
            
        elif syntax_list['name'] == 'show':
            return {
                'type': 'plot',
                'series': args[0],
                'title': args[1] if len(args) > 1 else '',
                'color': args[2] if len(args) > 2 else '#000000',
                'linewidth': args[3] if len(args) > 3 else 1,
                'style': args[4] if len(args) > 4 else 'line'
            }
            
        elif syntax_list['name'] == 'showshape':
            return {
                'type': 'shape',
                'location': args[0],
                'shape': args[1],
                'color': args[2] if len(args) > 2 else '#000000',
                'size': args[3] if len(args) > 3 else 'normal',
                'text': args[4] if len(args) > 4 else ''
            }
            
        elif syntax_list['name'] == 'showcond':
            return {
                'type': 'plot_condition',
                'condition': args[0],
                'title': args[1] if len(args) > 1 else '',
                'color': args[2] if len(args) > 2 else '#000000',
                'linewidth': args[3] if len(args) > 3 else 1,
                'style': args[4] if len(args) > 4 else 'line'
            }
            
        elif syntax_list['name'] == 'solid':
            return {
                'line_style': 'solid',
                'pattern': []
            }
            
        elif syntax_list['name'] == 'dotted':
            return {
                'line_style': 'dotted',
                'pattern': [1, 1]
            }
            
        elif syntax_list['name'] == 'dashed':
            return {
                'line_style': 'dashed',
                'pattern': [5, 5]
            }
            
        elif syntax_list['name'] == 'fontFamilyDefault':
            return {
                'font': 'Arial',
                'type': 'default'
            }
            
        elif syntax_list['name'] == 'fontFamilyMonospace':
            return {
                'font': 'Courier New',
                'type': 'monospace'
            }
            
        elif syntax_list['name'] == 'extendBoth':
            return {
                'extend': 'both',
                'plot_range': {'start': -999999, 'end': 999999},
                'visibility': {'past': True, 'future': True}
            }
            
        elif syntax_list['name'] == 'extendLeft':
            return {
                'extend': 'left',
                'plot_range': {'start': -999999, 'end': 0},
                'visibility': {'past': True, 'future': False}
            }
            
        elif syntax_list['name'] == 'extendNone':
            return {
                'extend': 'none',
                'plot_range': {'start': 0, 'end': 0},
                'visibility': {'past': False, 'future': False}
            }
            
        elif syntax_list['name'] == 'extendRight':
            return {
                'extend': 'right',
                'plot_range': {'start': 0, 'end': 999999},
                'visibility': {'past': False, 'future': True}
            }
            
        elif syntax_list['name'] == 'hlineStyleDashed':
            return {
                'style': 'dashed',
                'pattern': [5, 5],
                'type': 'horizontal'
            }
            
        elif syntax_list['name'] == 'hlineStyleDotted':
            return {
                'style': 'dotted',
                'pattern': [1, 1],
                'type': 'horizontal'
            }
            
        elif syntax_list['name'] == 'hlineStyleSolid':
            return {
                'style': 'solid',
                'pattern': [],
                'type': 'horizontal'
            }

        elif syntax_list['name'] == 'dayOfMonth':
            timestamp = args[0]
            days_since_epoch = timestamp // 86400
            year = 1970 + (days_since_epoch // 365.25)
            day_of_year = days_since_epoch % 365.25
            month_days = [31, 28 + (year % 4 == 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            month = 0
            while day_of_year > month_days[month]:
                day_of_year -= month_days[month]
                month += 1
            return int(day_of_year)
            
        elif syntax_list['name'] == 'dayOfWeek':
            timestamp = args[0]
            days_since_epoch = timestamp // 86400
            return int((days_since_epoch + 4) % 7)
            
        elif syntax_list['name'] == 'hour':
            timestamp = args[0]
            return int((timestamp % 86400) // 3600)
            
        elif syntax_list['name'] == 'minute':
            timestamp = args[0]
            return int((timestamp % 3600) // 60)
            
        elif syntax_list['name'] == 'month':
            timestamp = args[0]
            days_since_epoch = timestamp // 86400
            year = 1970 + (days_since_epoch // 365.25)
            day_of_year = days_since_epoch % 365.25
            month_days = [31, 28 + (year % 4 == 0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            month = 0
            while day_of_year > month_days[month]:
                day_of_year -= month_days[month]
                month += 1
            return month + 1
            
        elif syntax_list['name'] == 'second':
            timestamp = args[0]
            return int(timestamp % 60)
            
        elif syntax_list['name'] == 'time':
            current_bar = args[0]
            return current_bar['timestamp']
            
        elif syntax_list['name'] == 'timeClose':
            current_bar = args[0]
            return current_bar['timestamp'] + current_bar['duration']
            
        elif syntax_list['name'] == 'timeTradingDay':
            current_bar = args[0]
            day_start = current_bar['timestamp'] - (current_bar['timestamp'] % 86400)
            market_open = day_start + current_bar['session']['market_open_offset']
            return market_open
            
        elif syntax_list['name'] == 'timeNow':
            return int(time.time())
            
        elif syntax_list['name'] == 'weekOfYear':
            timestamp = args[0]
            days_since_epoch = timestamp // 86400
            year = 1970 + (days_since_epoch // 365.25)
            day_of_year = days_since_epoch % 365.25
            return int((day_of_year + 10) // 7)
            
        elif syntax_list['name'] == 'year':
            timestamp = args[0]
            days_since_epoch = timestamp // 86400
            return int(1970 + (days_since_epoch // 365.25))

        elif syntax_list['name'] == 'sessionIsFirstBar':
            bar_data = args[0]
            session_start = bar_data['session_start']
            current_time = bar_data['timestamp']
            return current_time == session_start
            
        elif syntax_list['name'] == 'sessionIsFirstBarRegular':
            bar_data = args[0]
            regular_session_start = bar_data['regular_session_start']
            current_time = bar_data['timestamp']
            return current_time == regular_session_start
            
        elif syntax_list['name'] == 'sessionIsLastBar':
            bar_data = args[0]
            session_end = bar_data['session_end']
            current_time = bar_data['timestamp']
            bar_duration = bar_data['duration']
            return current_time + bar_duration == session_end
            
        elif syntax_list['name'] == 'sessionIsLastBarRegular':
            bar_data = args[0]
            regular_session_end = bar_data['regular_session_end']
            current_time = bar_data['timestamp']
            bar_duration = bar_data['duration']
            return current_time + bar_duration == regular_session_end
            
        elif syntax_list['name'] == 'sessionIsMarket':
            bar_data = args[0]
            current_time = bar_data['timestamp']
            market_start = bar_data['market_session_start']
            market_end = bar_data['market_session_end']
            return market_start <= current_time < market_end
            
        elif syntax_list['name'] == 'sessionIsPostMarket':
            bar_data = args[0]
            current_time = bar_data['timestamp']
            market_end = bar_data['market_session_end']
            session_end = bar_data['session_end']
            return market_end <= current_time < session_end
            
        elif syntax_list['name'] == 'sessionIsPreMarket':
            bar_data = args[0]
            current_time = bar_data['timestamp']
            session_start = bar_data['session_start']
            market_start = bar_data['market_session_start']
            return session_start <= current_time < market_start

        elif syntax_list['name'] == 'boxAll':
            chart_data = args[0]
            boxes = []
            for box in chart_data['boxes']:
                boxes.append({
                    'id': box['id'],
                    'left': box['left'],
                    'top': box['top'],
                    'right': box['right'],
                    'bottom': box['bottom'],
                    'border_color': box['border_color'],
                    'background_color': box['background_color'],
                    'text': box['text']
                })
            return boxes
            
        elif syntax_list['name'] == 'chartBgCol':
            chart_data = args[0]
            return chart_data['background_color']
            
        elif syntax_list['name'] == 'chartFgCol':
            chart_data = args[0]
            return chart_data['foreground_color']
            
        elif syntax_list['name'] == 'chartIsHeikinAshi':
            chart_data = args[0]
            return chart_data['chart_type'] == 'heikin_ashi'
            
        elif syntax_list['name'] == 'chartIsKagi':
            chart_data = args[0]
            return chart_data['chart_type'] == 'kagi'
            
        elif syntax_list['name'] == 'chartIsLineBreak':
            chart_data = args[0]
            return chart_data['chart_type'] == 'line_break'
            
        elif syntax_list['name'] == 'chartIsPnf':
            chart_data = args[0]
            return chart_data['chart_type'] == 'point_and_figure'
            
        elif syntax_list['name'] == 'chartIsRange':
            chart_data = args[0]
            return chart_data['chart_type'] == 'range'
            
        elif syntax_list['name'] == 'chartIsRenko':
            chart_data = args[0]
            return chart_data['chart_type'] == 'renko'
            
        elif syntax_list['name'] == 'chartIsStandard':
            chart_data = args[0]
            return chart_data['chart_type'] == 'standard'
            
        elif syntax_list['name'] == 'chartLeftVisibleBarTime':
            chart_data = args[0]
            return chart_data['visible_range']['left_bar_time']
            
        elif syntax_list['name'] == 'chartRightVisibleBarTime':
            chart_data = args[0]
            return chart_data['visible_range']['right_bar_time']

        elif syntax_list['name'] == 'labelAll':
            chart_data = args[0]
            labels = []
            for label in chart_data['labels']:
                labels.append({
                    'id': label['id'],
                    'x': label['x'],
                    'y': label['y'],
                    'text': label['text'],
                    'color': label['color'],
                    'style': label['style'],
                    'size': label['size']
                })
            return labels
            
        elif syntax_list['name'] == 'lineAll':
            chart_data = args[0]
            lines = []
            for line in chart_data['lines']:
                lines.append({
                    'id': line['id'],
                    'x1': line['x1'],
                    'y1': line['y1'],
                    'x2': line['x2'],
                    'y2': line['y2'],
                    'color': line['color'],
                    'width': line['width'],
                    'style': line['style']
                })
            return lines
            
        elif syntax_list['name'] == 'lineFillAll':
            chart_data = args[0]
            fills = []
            for fill in chart_data['line_fills']:
                fills.append({
                    'id': fill['id'],
                    'line1_id': fill['line1_id'],
                    'line2_id': fill['line2_id'],
                    'color': fill['color'],
                    'transparency': fill['transparency']
                })
            return fills
            
        elif syntax_list['name'] == 'polylineAll':
            chart_data = args[0]
            polylines = []
            for polyline in chart_data['polylines']:
                polylines.append({
                    'id': polyline['id'],
                    'points': polyline['points'],
                    'color': polyline['color'],
                    'width': polyline['width'],
                    'style': polyline['style']
                })
            return polylines
            
        elif syntax_list['name'] == 'tableAll':
            chart_data = args[0]
            tables = []
            for table in chart_data['tables']:
                tables.append({
                    'id': table['id'],
                    'position': table['position'],
                    'rows': table['rows'],
                    'columns': table['columns'],
                    'cells': table['cells'],
                    'colors': table['colors'],
                    'borders': table['borders']
                })
            return tables

        elif syntax_list['name'] == 'andOp':
            left_operand = args[0]
            right_operand = args[1]
            return bool(left_operand and right_operand)
            
        elif syntax_list['name'] == 'enumType':
            enum_name = args[0]
            enum_values = args[1]
            enum_dict = {}
            for i, value in enumerate(enum_values):
                enum_dict[value] = i
            return {
                'name': enum_name,
                'values': enum_dict,
                'type': 'enum'
            }
            
        elif syntax_list['name'] == 'exportFunc':
            export_name = args[0]
            export_value = args[1]
            return {
                'name': export_name,
                'value': export_value,
                'type': 'export'
            }
            
        elif syntax_list['name'] == 'forLoop':
            init_value = args[0]
            condition = args[1]
            increment = args[2]
            body = args[3]
            results = []
            current = init_value
            
            while condition(current):
                results.append(body(current))
                current = increment(current)
            return results
            
        elif syntax_list['name'] == 'forInLoop':
            iterable = args[0]
            body = args[1]
            results = []
            
            for item in iterable:
                results.append(body(item))
            return results
            
        elif syntax_list['name'] == 'ifCond':
            condition = args[0]
            true_branch = args[1]
            false_branch = args[2] if len(args) > 2 else None
            
            if condition:
                return true_branch
            elif false_branch is not None:
                return false_branch
            return None
            
        elif syntax_list['name'] == 'importFunc':
            module_path = args[0]
            import_options = args[1] if len(args) > 1 else {}
            return {
                'path': module_path,
                'options': import_options,
                'type': 'import'
            }

        elif syntax_list['name'] == 'methodFunc':
            method_name = args[0]
            parameters = args[1]
            body = args[2]
            return {
                'name': method_name,
                'parameters': parameters,
                'body': body,
                'type': 'method'
            }
            
        elif syntax_list['name'] == 'notOp':
            operand = args[0]
            return not bool(operand)
            
        elif syntax_list['name'] == 'orOp':
            left_operand = args[0]
            right_operand = args[1]
            return bool(left_operand or right_operand)
            
        elif syntax_list['name'] == 'switchCase':
            value = args[0]
            cases = args[1]
            default = args[2] if len(args) > 2 else None
            
            for case in cases:
                if case['value'] == value:
                    return case['body']
            return default
            
        elif syntax_list['name'] == 'typeDef':
            type_name = args[0]
            type_definition = args[1]
            return {
                'name': type_name,
                'definition': type_definition,
                'type': 'typedef'
            }
            
        elif syntax_list['name'] == 'let':
            variable_name = args[0]
            initial_value = args[1]
            return {
                'name': variable_name,
                'value': initial_value,
                'type': 'variable',
                'mutable': True
            }
            
        elif syntax_list['name'] == 'letip':
            variable_name = args[0]
            initial_value = args[1]
            return {
                'name': variable_name,
                'value': initial_value,
                'type': 'variable',
                'mutable': False
            }
            
        elif syntax_list['name'] == 'whileLoop':
            condition = args[0]
            body = args[1]
            results = []
            
            while condition():
                results.append(body())
            return results

        

        # market data

        elif syntax_list['name'] == 'open':
            return args[0][0]
            
        elif syntax_list['name'] == 'high':
            return args[0][1]
            
        elif syntax_list['name'] == 'low':
            return args[0][2]
            
        elif syntax_list['name'] == 'close':
            return args[0][3]
            
        elif syntax_list['name'] == 'volume':
            return args[0][4]
            
        elif syntax_list['name'] == 'hl2':
            return (args[0][1] + args[0][2]) / 2
            
        elif syntax_list['name'] == 'hlc3':
            return (args[0][1] + args[0][2] + args[0][3]) / 3
            
        elif syntax_list['name'] == 'hlcc4':
            return (args[0][1] + args[0][2] + args[0][3] + args[0][3]) / 4
            
        elif syntax_list['name'] == 'ohlc4':
            return (args[0][0] + args[0][1] + args[0][2] + args[0][3]) / 4
            
        elif syntax_list['name'] == 'symInfoMinMove':
            return {
                'type': 'numeric',
                'value': args[0]['instrument_details']['minimum_price_movement'],
                'decimals': args[0]['instrument_details']['price_decimals']
            }
            
        elif syntax_list['name'] == 'symInfoMinTick':
            return {
                'type': 'numeric',
                'value': args[0]['instrument_details']['minimum_tick_size'],
                'decimals': args[0]['instrument_details']['price_decimals']
            }
            
        elif syntax_list['name'] == 'symInfoPointValue':
            return {
                'type': 'numeric',
                'value': args[0]['instrument_details']['contract_size'],
                'currency': args[0]['instrument_details']['currency']
            }
            
        elif syntax_list['name'] == 'symInfoPrefix':
            return {
                'type': 'string',
                'exchange': args[0]['exchange']['code'],
                'market': args[0]['market']['code'],
                'value': args[0]['exchange']['code'] + ':' + args[0]['market']['code']
            }
            
        elif syntax_list['name'] == 'symInfoPriceScale':
            return {
                'type': 'numeric',
                'value': 10 ** args[0]['instrument_details']['price_decimals'],
                'decimals': args[0]['instrument_details']['price_decimals']
            }
            
        elif syntax_list['name'] == 'symInfoRoot':
            return {
                'type': 'string',
                'value': args[0]['instrument_details']['root_symbol'],
                'description': args[0]['instrument_details']['description']
            }
            
        elif syntax_list['name'] == 'symInfoSector':
            return {
                'type': 'string',
                'sector': args[0]['company']['sector'],
                'industry': args[0]['company']['industry'],
                'category': args[0]['company']['category']
            }
            
        elif syntax_list['name'] == 'symInfoSession':
            return {
                'type': 'object',
                'regular': {
                    'start': args[0]['session']['regular']['start'],
                    'end': args[0]['session']['regular']['end'],
                    'timezone': args[0]['session']['timezone']
                },
                'extended': {
                    'pre_market': {
                        'start': args[0]['session']['pre_market']['start'],
                        'end': args[0]['session']['pre_market']['end']
                    },
                    'post_market': {
                        'start': args[0]['session']['post_market']['start'],
                        'end': args[0]['session']['post_market']['end']
                    }
                }
            }
            
        elif syntax_list['name'] == 'symInfoShareholders':
            return {
                'type': 'object',
                'institutional': {
                    'count': args[0]['shareholders']['institutional']['count'],
                    'ownership_percent': args[0]['shareholders']['institutional']['ownership_percent']
                },
                'individual': {
                    'count': args[0]['shareholders']['individual']['count'],
                    'ownership_percent': args[0]['shareholders']['individual']['ownership_percent']
                }
            }
            
        elif syntax_list['name'] == 'symInfoSharesOutstandingFloat':
            return {
                'type': 'numeric',
                'value': args[0]['shares']['float'],
                'last_update': args[0]['shares']['float_date']
            }
            
        elif syntax_list['name'] == 'symInfoSharesOutstandingTotal':
            return {
                'type': 'numeric',
                'value': args[0]['shares']['total'],
                'last_update': args[0]['shares']['total_date']
            }



        # ta indicators

        elif syntax_list['name'] == 'sma':
            period = args[1]
            values = args[0]
            if len(values) < period:
                return float('nan')
            return sum(values[-period:]) / period
            
        elif syntax_list['name'] == 'ema':
            period = args[1]
            values = args[0]
            if len(values) < period:
                return float('nan')
            alpha = 2 / (period + 1)
            result = values[0]
            for i in range(1, len(values)):
                result = alpha * values[i] + (1 - alpha) * result
            return result
            
        elif syntax_list['name'] == 'rsi':
            period = args[1]
            values = args[0]
            if len(values) < period + 1:
                return float('nan')
            gains = []
            losses = []
            for i in range(1, len(values)):
                change = values[i] - values[i-1]
                gains.append(max(change, 0))
                losses.append(max(-change, 0))
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            if avg_loss == 0:
                return 100
            rs = avg_gain / avg_loss
            return 100 - (100 / (1 + rs))
            
        elif syntax_list['name'] == 'minvalue':
            return min(args[0])
            
        elif syntax_list['name'] == 'maxvalue':
            return max(args[0])
            
        elif syntax_list['name'] == 'taAccDist':
            high = args[0]
            low = args[1]
            close = args[2]
            volume = args[3]
            mfm = ((close - low) - (high - close)) / (high - low) if high != low else 0
            return mfm * volume
            
        elif syntax_list['name'] == 'taIII':
            high = args[0]
            low = args[1]
            close = args[2]
            volume = args[3]
            return (2 * close - high - low) / (high - low) * volume if high != low else 0
            
        elif syntax_list['name'] == 'taNVI':
            close = args[0]
            volume = args[1]
            if len(close) < 2:
                return 1000
            prev_volume = volume[-2]
            curr_volume = volume[-1]
            if curr_volume < prev_volume:
                return (close[-1] - close[-2]) / close[-2] * 1000
            return 1000
            
        elif syntax_list['name'] == 'taOBV':
            close = args[0]
            volume = args[1]
            if len(close) < 2:
                return 0
            prev_close = close[-2]
            curr_close = close[-1]
            if curr_close > prev_close:
                return volume[-1]
            elif curr_close < prev_close:
                return -volume[-1]
            return 0
            
        elif syntax_list['name'] == 'taPVI':
            close = args[0]
            volume = args[1]
            if len(close) < 2:
                return 1000
            prev_volume = volume[-2]
            curr_volume = volume[-1]
            if curr_volume > prev_volume:
                return (close[-1] - close[-2]) / close[-2] * 1000
            return 1000
            
        elif syntax_list['name'] == 'taPVT':
            close = args[0]
            volume = args[1]
            if len(close) < 2:
                return 0
            return ((close[-1] - close[-2]) / close[-2]) * volume[-1]
            
        elif syntax_list['name'] == 'taTR':
            high = args[0]
            low = args[1]
            close = args[2]
            if len(close) < 2:
                return high[-1] - low[-1]
            prev_close = close[-2]
            return max(high[-1] - low[-1], abs(high[-1] - prev_close), abs(low[-1] - prev_close))
            
        elif syntax_list['name'] == 'taVWAP':
            high = args[0]
            low = args[1]
            close = args[2]
            volume = args[3]
            typical_price = (high + low + close) / 3
            return sum(typical_price * volume) / sum(volume)

        elif syntax_list['name'] == 'taWAD':
            high = args[0]
            low = args[1]
            close = args[2]
            if len(close) < 2:
                return 0
            prev_close = close[-2]
            if close[-1] > prev_close:
                return close[-1] - min(low[-1], prev_close)
            else:
                return close[-1] - max(high[-1], prev_close)
                
        elif syntax_list['name'] == 'taWVAD':
            high = args[0]
            low = args[1]
            close = args[2]
            volume = args[3]
            if len(close) < 2:
                return 0
            prev_close = close[-2]
            if close[-1] > prev_close:
                return (close[-1] - min(low[-1], prev_close)) * volume[-1]
            else:
                return (close[-1] - max(high[-1], prev_close)) * volume[-1]
                
        elif syntax_list['name'] == 'taAlma':
            data = args[0]
            window = args[1]
            offset = args[2]
            sigma = args[3]
            m = offset * (window - 1)
            s = window / sigma
            weights = []
            norm = 0
            
            for i in range(window):
                w = exp(-((i - m) * (i - m)) / (2 * s * s))
                weights.append(w)
                norm += w
                
            for i in range(window):
                weights[i] /= norm
                
            result = 0
            for i in range(window):
                result += data[-i-1] * weights[i]
            return result
            
        elif syntax_list['name'] == 'taAtr':
            high = args[0]
            low = args[1]
            close = args[2]
            period = args[3]
            tr_values = []
            
            for i in range(len(close)):
                if i == 0:
                    tr = high[i] - low[i]
                else:
                    tr = max(high[i] - low[i],
                            abs(high[i] - close[i-1]),
                            abs(low[i] - close[i-1]))
                tr_values.append(tr)
                
            if len(tr_values) < period:
                return float('nan')
                
            return sum(tr_values[-period:]) / period
        
        elif syntax_list['name'] == 'taBarsSince':
            condition = args[0]
            count = 0
            for i in reversed(range(len(condition))):
                if not condition[i]:
                    count += 1
                else:
                    break
            return count
            
        elif syntax_list['name'] == 'taBb':
            data = args[0]
            period = args[1]
            mult = args[2]
            if len(data) < period:
                return float('nan')
            sma = sum(data[-period:]) / period
            variance = sum((x - sma) ** 2 for x in data[-period:]) / period
            std = variance ** 0.5
            return {
                'middle': sma,
                'upper': sma + mult * std,
                'lower': sma - mult * std
            }
            
        elif syntax_list['name'] == 'taBbw':
            data = args[0]
            period = args[1]
            mult = args[2]
            if len(data) < period:
                return float('nan')
            sma = sum(data[-period:]) / period
            variance = sum((x - sma) ** 2 for x in data[-period:]) / period
            std = variance ** 0.5
            return ((sma + mult * std) - (sma - mult * std)) / sma * 100
            
        elif syntax_list['name'] == 'taCci':
            high = args[0]
            low = args[1]
            close = args[2]
            period = args[3]
            if len(close) < period:
                return float('nan')
            tp = [(h + l + c) / 3 for h, l, c in zip(high[-period:], low[-period:], close[-period:])]
            sma = sum(tp) / period
            mean_dev = sum(abs(x - sma) for x in tp) / period
            return (tp[-1] - sma) / (0.015 * mean_dev) if mean_dev != 0 else 0
            
        elif syntax_list['name'] == 'taChange':
            data = args[0]
            if len(data) < 2:
                return float('nan')
            return data[-1] - data[-2]
            
        elif syntax_list['name'] == 'taCmo':
            data = args[0]
            period = args[1]
            if len(data) < period + 1:
                return float('nan')
            ups = []
            downs = []
            for i in range(1, period + 1):
                change = data[-i] - data[-i-1]
                ups.append(max(change, 0))
                downs.append(max(-change, 0))
            sum_ups = sum(ups)
            sum_downs = sum(downs)
            return 100 * (sum_ups - sum_downs) / (sum_ups + sum_downs) if (sum_ups + sum_downs) != 0 else 0

        elif syntax_list['name'] == 'taCog':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            numerator = 0
            denominator = 0
            for i in range(period):
                numerator += (i + 1) * data[-i-1]
                denominator += data[-i-1]
            return -numerator / denominator if denominator != 0 else 0
            
        elif syntax_list['name'] == 'taCorrelation':
            data1 = args[0]
            data2 = args[1]
            period = args[2]
            if len(data1) < period or len(data2) < period:
                return float('nan')
            x = data1[-period:]
            y = data2[-period:]
            mean_x = sum(x) / period
            mean_y = sum(y) / period
            covar = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(period))
            var_x = sum((val - mean_x) ** 2 for val in x)
            var_y = sum((val - mean_y) ** 2 for val in y)
            return covar / ((var_x * var_y) ** 0.5) if var_x != 0 and var_y != 0 else 0
            
        elif syntax_list['name'] == 'taCross':
            data1 = args[0]
            data2 = args[1]
            if len(data1) < 2 or len(data2) < 2:
                return False
            return (data1[-2] <= data2[-2] and data1[-1] > data2[-1]) or (data1[-2] >= data2[-2] and data1[-1] < data2[-1])
            
        elif syntax_list['name'] == 'taCrossover':
            data1 = args[0]
            data2 = args[1]
            if len(data1) < 2 or len(data2) < 2:
                return False
            return data1[-2] <= data2[-2] and data1[-1] > data2[-1]
            
        elif syntax_list['name'] == 'taCrossunder':
            data1 = args[0]
            data2 = args[1]
            if len(data1) < 2 or len(data2) < 2:
                return False
            return data1[-2] >= data2[-2] and data1[-1] < data2[-1]
            
        elif syntax_list['name'] == 'taCum':
            data = args[0]
            result = 0
            for value in data:
                result += value
            return result

        elif syntax_list['name'] == 'taDev':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            mean = sum(data[-period:]) / period
            return sum(abs(x - mean) for x in data[-period:]) / period
            
        elif syntax_list['name'] == 'taDmi':
            high = args[0]
            low = args[1]
            period = args[2]
            if len(high) < period + 1:
                return float('nan')
            tr_list = []
            plus_dm_list = []
            minus_dm_list = []
            
            for i in range(1, len(high)):
                tr = max(high[i] - low[i],
                        abs(high[i] - low[i-1]),
                        abs(low[i] - high[i-1]))
                plus_dm = max(high[i] - high[i-1], 0) if high[i] - high[i-1] > low[i-1] - low[i] else 0
                minus_dm = max(low[i-1] - low[i], 0) if low[i-1] - low[i] > high[i] - high[i-1] else 0
                tr_list.append(tr)
                plus_dm_list.append(plus_dm)
                minus_dm_list.append(minus_dm)
                
            tr_sum = sum(tr_list[-period:])
            plus_dm_sum = sum(plus_dm_list[-period:])
            minus_dm_sum = sum(minus_dm_list[-period:])
            
            plus_di = 100 * plus_dm_sum / tr_sum if tr_sum != 0 else 0
            minus_di = 100 * minus_dm_sum / tr_sum if tr_sum != 0 else 0
            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di) if (plus_di + minus_di) != 0 else 0
            
            return {
                'plus_di': plus_di,
                'minus_di': minus_di,
                'dx': dx
            }
            
        elif syntax_list['name'] == 'taEma':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            alpha = 2 / (period + 1)
            result = data[0]
            for i in range(1, len(data)):
                result = alpha * data[i] + (1 - alpha) * result
            return result
            
        elif syntax_list['name'] == 'taFalling':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return False
            for i in range(1, period):
                if data[-i] >= data[-i-1]:
                    return False
            return True

        elif syntax_list['name'] == 'taHighest':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return max(data[-period:])
            
        elif syntax_list['name'] == 'taHighestBars':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            highest = max(data[-period:])
            for i in range(period):
                if data[-i-1] == highest:
                    return i
            return 0
            
        elif syntax_list['name'] == 'taHma':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            
            half_period = period // 2
            sqrt_period = int(period ** 0.5)
            
            wma1 = []
            wma2 = []
            for i in range(len(data) - period + 1):
                sum1 = sum((j + 1) * data[i + j] for j in range(half_period))
                div1 = sum(j + 1 for j in range(half_period))
                wma1.append(sum1 / div1 if div1 != 0 else 0)
                
                sum2 = sum((j + 1) * data[i + j] for j in range(period))
                div2 = sum(j + 1 for j in range(period))
                wma2.append(sum2 / div2 if div2 != 0 else 0)
            
            raw = [2 * wma1[i] - wma2[i] for i in range(len(wma1))]
            
            final_sum = sum((j + 1) * raw[-(sqrt_period-j)] for j in range(sqrt_period))
            final_div = sum(j + 1 for j in range(sqrt_period))
            
            return final_sum / final_div if final_div != 0 else 0
            
        elif syntax_list['name'] == 'taKc':
            high = args[0]
            low = args[1]
            close = args[2]
            period = args[3]
            mult = args[4]
            if len(close) < period:
                return float('nan')
                
            typical_prices = [(h + l + c) / 3 for h, l, c in zip(high[-period:], low[-period:], close[-period:])]
            sma = sum(typical_prices) / period
            
            mean_dev = sum(abs(tp - sma) for tp in typical_prices) / period
            
            return {
                'middle': sma,
                'upper': sma + mult * mean_dev,
                'lower': sma - mult * mean_dev
            }

        elif syntax_list['name'] == 'taKcw':
            high = args[0]
            low = args[1]
            close = args[2]
            period = args[3]
            mult = args[4]
            if len(close) < period:
                return float('nan')
                
            typical_prices = [(h + l + c) / 3 for h, l, c in zip(high[-period:], low[-period:], close[-period:])]
            sma = sum(typical_prices) / period
            mean_dev = sum(abs(tp - sma) for tp in typical_prices) / period
            
            return (2 * mult * mean_dev) / sma * 100
            
        elif syntax_list['name'] == 'taLinReg':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
                
            x = list(range(period))
            y = data[-period:]
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x[i] * y[i] for i in range(period))
            sum_xx = sum(x[i] * x[i] for i in range(period))
            
            slope = (period * sum_xy - sum_x * sum_y) / (period * sum_xx - sum_x * sum_x)
            intercept = (sum_y - slope * sum_x) / period
            
            return slope * (period - 1) + intercept
            
        elif syntax_list['name'] == 'taLowest':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return min(data[-period:])
            
        elif syntax_list['name'] == 'taLowestBars':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            lowest = min(data[-period:])
            for i in range(period):
                if data[-i-1] == lowest:
                    return i
            return 0
            
        elif syntax_list['name'] == 'taMacd':
            data = args[0]
            fast_length = args[1]
            slow_length = args[2]
            signal_length = args[3]
            if len(data) < max(fast_length, slow_length, signal_length):
                return float('nan')
                
            alpha_fast = 2 / (fast_length + 1)
            alpha_slow = 2 / (slow_length + 1)
            alpha_signal = 2 / (signal_length + 1)
            
            ema_fast = data[0]
            ema_slow = data[0]
            for price in data[1:]:
                ema_fast = alpha_fast * price + (1 - alpha_fast) * ema_fast
                ema_slow = alpha_slow * price + (1 - alpha_slow) * ema_slow
                
            macd_line = ema_fast - ema_slow
            signal_line = alpha_signal * macd_line + (1 - alpha_signal) * (ema_fast - ema_slow)
            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line,
                'signal': signal_line,
                'histogram': histogram
            }
        
        elif syntax_list['name'] == 'taMax':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return max(data[-period:])
            
        elif syntax_list['name'] == 'taMedian':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            sorted_data = sorted(data[-period:])
            mid = period // 2
            return sorted_data[mid] if period % 2 else (sorted_data[mid-1] + sorted_data[mid]) / 2
            
        elif syntax_list['name'] == 'taMfi':
            high = args[0]
            low = args[1]
            close = args[2]
            volume = args[3]
            period = args[4]
            if len(close) < period + 1:
                return float('nan')
                
            typical_prices = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
            money_flows = [tp * v for tp, v in zip(typical_prices, volume)]
            
            pos_flows = []
            neg_flows = []
            for i in range(1, len(typical_prices)):
                if typical_prices[i] > typical_prices[i-1]:
                    pos_flows.append(money_flows[i])
                    neg_flows.append(0)
                else:
                    pos_flows.append(0)
                    neg_flows.append(money_flows[i])
                    
            pos_sum = sum(pos_flows[-period:])
            neg_sum = sum(neg_flows[-period:])
            
            return 100 * pos_sum / (pos_sum + neg_sum) if (pos_sum + neg_sum) != 0 else 50
            
        elif syntax_list['name'] == 'taMin':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return min(data[-period:])
            
        elif syntax_list['name'] == 'taMode':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            values = data[-period:]
            counts = {}
            for value in values:
                counts[value] = counts.get(value, 0) + 1
            max_count = max(counts.values())
            modes = [k for k, v in counts.items() if v == max_count]
            return modes[0]

        elif syntax_list['name'] == 'taMom':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return data[-1] - data[-period]
            
        elif syntax_list['name'] == 'taPercentile':
            data = args[0]
            period = args[1]
            percentage = args[2]
            if len(data) < period:
                return float('nan')
            sorted_data = sorted(data[-period:])
            index = (period - 1) * percentage / 100
            lower_idx = int(index)
            fraction = index - lower_idx
            if lower_idx + 1 >= period:
                return sorted_data[-1]
            return sorted_data[lower_idx] + fraction * (sorted_data[lower_idx + 1] - sorted_data[lower_idx])
            
        elif syntax_list['name'] == 'taPercentRank':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            current = data[-1]
            window = data[-period:]
            count = sum(1 for x in window if x < current)
            return 100 * count / (period - 1)
            
        elif syntax_list['name'] == 'taPivotHigh':
            data = args[0]
            left_bars = args[1]
            right_bars = args[2]
            if len(data) < left_bars + right_bars + 1:
                return float('nan')
            center_idx = -right_bars - 1
            value = data[center_idx]
            for i in range(-right_bars - left_bars - 1, -right_bars):
                if data[i] > value:
                    return float('nan')
            for i in range(-right_bars, 0):
                if data[i] >= value:
                    return float('nan')
            return value
            
        elif syntax_list['name'] == 'taPivotLow':
            data = args[0]
            left_bars = args[1]
            right_bars = args[2]
            if len(data) < left_bars + right_bars + 1:
                return float('nan')
            center_idx = -right_bars - 1
            value = data[center_idx]
            for i in range(-right_bars - left_bars - 1, -right_bars):
                if data[i] < value:
                    return float('nan')
            for i in range(-right_bars, 0):
                if data[i] <= value:
                    return float('nan')
            return value

        elif syntax_list['name'] == 'taRange':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return max(data[-period:]) - min(data[-period:])
            
        elif syntax_list['name'] == 'taRising':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return False
            for i in range(1, period):
                if data[-i] <= data[-i-1]:
                    return False
            return True
            
        elif syntax_list['name'] == 'taRma':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            alpha = 1 / period
            result = sum(data[:period]) / period
            for i in range(period, len(data)):
                result = alpha * data[i] + (1 - alpha) * result
            return result
            
        elif syntax_list['name'] == 'taRoc':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return ((data[-1] - data[-period]) / data[-period]) * 100 if data[-period] != 0 else float('nan')
            
        elif syntax_list['name'] == 'taRsi':
            data = args[0]
            period = args[1]
            if len(data) < period + 1:
                return float('nan')
            gains = []
            losses = []
            for i in range(1, len(data)):
                change = data[i] - data[i-1]
                gains.append(max(change, 0))
                losses.append(max(-change, 0))
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            if avg_loss == 0:
                return 100
            rs = avg_gain / avg_loss
            return 100 - (100 / (1 + rs))

        elif syntax_list['name'] == 'taSar':
            high = args[0]
            low = args[1]
            acceleration = args[2]
            maximum = args[3]
            if len(high) < 2:
                return float('nan')
            trend = 1  # 1 for up, -1 for down
            sar = low[0]
            extreme_point = high[0]
            acc_factor = acceleration
            
            for i in range(1, len(high)):
                if trend == 1:
                    sar = sar + acc_factor * (extreme_point - sar)
                    if low[i] < sar:
                        trend = -1
                        sar = extreme_point
                        extreme_point = low[i]
                        acc_factor = acceleration
                    else:
                        if high[i] > extreme_point:
                            extreme_point = high[i]
                            acc_factor = min(acc_factor + acceleration, maximum)
                else:
                    sar = sar - acc_factor * (sar - extreme_point)
                    if high[i] > sar:
                        trend = 1
                        sar = extreme_point
                        extreme_point = high[i]
                        acc_factor = acceleration
                    else:
                        if low[i] < extreme_point:
                            extreme_point = low[i]
                            acc_factor = min(acc_factor + acceleration, maximum)
            return sar
            
        elif syntax_list['name'] == 'taSma':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            return sum(data[-period:]) / period
            
        elif syntax_list['name'] == 'taStdev':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            mean = sum(data[-period:]) / period
            squared_diff_sum = sum((x - mean) ** 2 for x in data[-period:])
            return (squared_diff_sum / period) ** 0.5
            
        elif syntax_list['name'] == 'taStoch':
            high = args[0]
            low = args[1]
            close = args[2]
            period = args[3]
            smooth_k = args[4]
            smooth_d = args[5]
            if len(close) < period:
                return float('nan')
                
            k_raw = 100 * (close[-1] - min(low[-period:])) / (max(high[-period:]) - min(low[-period:]))
            k = sum([k_raw] * smooth_k) / smooth_k
            d = sum([k] * smooth_d) / smooth_d
            
            return {
                'k': k,
                'd': d
            }

        elif syntax_list['name'] == 'taSuperTrend':
            high = args[0]
            low = args[1]
            close = args[2]
            period = args[3]
            multiplier = args[4]
            if len(close) < period:
                return float('nan')
                
            tr_list = []
            for i in range(1, len(high)):
                tr = max(high[i] - low[i],
                        abs(high[i] - close[i-1]),
                        abs(low[i] - close[i-1]))
                tr_list.append(tr)
                
            atr = sum(tr_list[-period:]) / period
            
            upper_band = (high[-1] + low[-1]) / 2 + multiplier * atr
            lower_band = (high[-1] + low[-1]) / 2 - multiplier * atr
            
            supertrend = upper_band if close[-1] <= upper_band else lower_band
            
            return {
                'supertrend': supertrend,
                'direction': -1 if close[-1] > supertrend else 1
            }
            
        elif syntax_list['name'] == 'taSwma':
            data = args[0]
            if len(data) < 4:
                return float('nan')
            weights = [1/6, 2/6, 2/6, 1/6]
            return sum(w * d for w, d in zip(weights, data[-4:]))
            
        elif syntax_list['name'] == 'taTsi':
            data = args[0]
            r_period = args[1]
            s_period = args[2]
            if len(data) < max(r_period, s_period):
                return float('nan')
                
            momentum = [data[i] - data[i-1] for i in range(1, len(data))]
            
            smooth1 = []
            value = momentum[0]
            for price in momentum[1:]:
                value = (2 / (r_period + 1)) * price + (1 - (2 / (r_period + 1))) * value
                smooth1.append(value)
                
            smooth2 = []
            value = smooth1[0]
            for price in smooth1[1:]:
                value = (2 / (s_period + 1)) * price + (1 - (2 / (s_period + 1))) * value
                smooth2.append(value)
                
            abs_momentum = [abs(x) for x in momentum]
            
            abs_smooth1 = []
            value = abs_momentum[0]
            for price in abs_momentum[1:]:
                value = (2 / (r_period + 1)) * price + (1 - (2 / (r_period + 1))) * value
                abs_smooth1.append(value)
                
            abs_smooth2 = []
            value = abs_smooth1[0]
            for price in abs_smooth1[1:]:
                value = (2 / (s_period + 1)) * price + (1 - (2 / (s_period + 1))) * value
                abs_smooth2.append(value)
                
            return 100 * (smooth2[-1] / abs_smooth2[-1]) if abs_smooth2[-1] != 0 else 0

        elif syntax_list['name'] == 'taValueWhen':
            condition = args[0]
            source = args[1]
            occurrence = args[2]
            if len(condition) != len(source):
                return float('nan')
            count = 0
            for i in reversed(range(len(condition))):
                if condition[i]:
                    if count == occurrence:
                        return source[i]
                    count += 1
            return float('nan')
            
        elif syntax_list['name'] == 'taVariance':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            mean = sum(data[-period:]) / period
            return sum((x - mean) ** 2 for x in data[-period:]) / period
            
        elif syntax_list['name'] == 'taVwap':
            high = args[0]
            low = args[1]
            close = args[2]
            volume = args[3]
            typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
            return sum(tp * v for tp, v in zip(typical_price, volume)) / sum(volume) if sum(volume) != 0 else float('nan')
            
        elif syntax_list['name'] == 'taVwma':
            data = args[0]
            volume = args[1]
            period = args[2]
            if len(data) < period:
                return float('nan')
            return sum(d * v for d, v in zip(data[-period:], volume[-period:])) / sum(volume[-period:]) if sum(volume[-period:]) != 0 else float('nan')
            
        elif syntax_list['name'] == 'taWma':
            data = args[0]
            period = args[1]
            if len(data) < period:
                return float('nan')
            weights = list(range(1, period + 1))
            weighted_sum = sum(w * d for w, d in zip(weights, data[-period:]))
            return weighted_sum / sum(weights)
            
        elif syntax_list['name'] == 'taWpr':
            high = args[0]
            low = args[1]
            close = args[2]
            period = args[3]
            if len(close) < period:
                return float('nan')
            highest_high = max(high[-period:])
            lowest_low = min(low[-period:])
            return -100 * (highest_high - close[-1]) / (highest_high - lowest_low) if (highest_high - lowest_low) != 0 else 0


        # strategy 

        elif syntax_list['name'] == 'strategyAccountCurrency':
            return args[0]['account']['currency']
            
        elif syntax_list['name'] == 'strategyAvgLosingTrade':
            total_loss = sum(trade['profit'] for trade in args[0]['closed_trades'] if trade['profit'] < 0)
            loss_count = sum(1 for trade in args[0]['closed_trades'] if trade['profit'] < 0)
            return total_loss / loss_count if loss_count > 0 else 0
            
        elif syntax_list['name'] == 'strategyAvgLosingTradePercent':
            total_loss_percent = sum(trade['profit_percent'] for trade in args[0]['closed_trades'] if trade['profit'] < 0)
            loss_count = sum(1 for trade in args[0]['closed_trades'] if trade['profit'] < 0)
            return total_loss_percent / loss_count if loss_count > 0 else 0
            
        elif syntax_list['name'] == 'strategyAvgTrade':
            total_profit = sum(trade['profit'] for trade in args[0]['closed_trades'])
            trade_count = len(args[0]['closed_trades'])
            return total_profit / trade_count if trade_count > 0 else 0
            
        elif syntax_list['name'] == 'strategyAvgTradePercent':
            total_profit_percent = sum(trade['profit_percent'] for trade in args[0]['closed_trades'])
            trade_count = len(args[0]['closed_trades'])
            return total_profit_percent / trade_count if trade_count > 0 else 0
            
        elif syntax_list['name'] == 'strategyAvgWinningTrade':
            total_win = sum(trade['profit'] for trade in args[0]['closed_trades'] if trade['profit'] > 0)
            win_count = sum(1 for trade in args[0]['closed_trades'] if trade['profit'] > 0)
            return total_win / win_count if win_count > 0 else 0
            
        elif syntax_list['name'] == 'strategyAvgWinningTradePercent':
            total_win_percent = sum(trade['profit_percent'] for trade in args[0]['closed_trades'] if trade['profit'] > 0)
            win_count = sum(1 for trade in args[0]['closed_trades'] if trade['profit'] > 0)
            return total_win_percent / win_count if win_count > 0 else 0
            
        elif syntax_list['name'] == 'strategyClosedTrades':
            return len(args[0]['closed_trades'])
            
        elif syntax_list['name'] == 'strategyClosedTradesFirstIndex':
            return args[0]['closed_trades'][0]['entry_bar_index'] if args[0]['closed_trades'] else 0
            
        elif syntax_list['name'] == 'strategyEquity':
            return args[0]['account']['initial_capital'] + args[0]['net_profit']
            
        elif syntax_list['name'] == 'strategyEvenTrades':
            return sum(1 for trade in args[0]['closed_trades'] if trade['profit'] == 0)

        elif syntax_list['name'] == 'strategyGrossLoss':
            return sum(trade['profit'] for trade in args[0]['closed_trades'] if trade['profit'] < 0)
            
        elif syntax_list['name'] == 'strategyGrossLossPercent':
            initial_capital = args[0]['account']['initial_capital']
            gross_loss = sum(trade['profit'] for trade in args[0]['closed_trades'] if trade['profit'] < 0)
            return (gross_loss / initial_capital) * 100 if initial_capital != 0 else 0
            
        elif syntax_list['name'] == 'strategyGrossProfit':
            return sum(trade['profit'] for trade in args[0]['closed_trades'] if trade['profit'] > 0)
            
        elif syntax_list['name'] == 'strategyGrossProfitPercent':
            initial_capital = args[0]['account']['initial_capital']
            gross_profit = sum(trade['profit'] for trade in args[0]['closed_trades'] if trade['profit'] > 0)
            return (gross_profit / initial_capital) * 100 if initial_capital != 0 else 0
            
        elif syntax_list['name'] == 'strategyInitialCapital':
            return args[0]['account']['initial_capital']
            
        elif syntax_list['name'] == 'strategyLossTrades':
            return sum(1 for trade in args[0]['closed_trades'] if trade['profit'] < 0)
            
        elif syntax_list['name'] == 'strategyMarginLiquidationPrice':
            position = args[0]['position']
            margin_requirement = args[0]['account']['margin_requirement']
            return position['entry_price'] * (1 - margin_requirement) if position['direction'] == 'long' else position['entry_price'] * (1 + margin_requirement)
            
        elif syntax_list['name'] == 'strategyMaxContractsHeldAll':
            return max(trade['contracts'] for trade in args[0]['all_trades'])
            
        elif syntax_list['name'] == 'strategyMaxContractsHeldLong':
            return max((trade['contracts'] for trade in args[0]['all_trades'] if trade['direction'] == 'long'), default=0)
            
        elif syntax_list['name'] == 'strategyMaxContractsHeldShort':
            return max((trade['contracts'] for trade in args[0]['all_trades'] if trade['direction'] == 'short'), default=0)

        elif syntax_list['name'] == 'strategyMaxDrawdown':
            equity_curve = []
            current_equity = args[0]['account']['initial_capital']
            for trade in args[0]['closed_trades']:
                current_equity += trade['profit']
                equity_curve.append(current_equity)
            
            max_drawdown = 0
            peak = equity_curve[0]
            for equity in equity_curve:
                if equity > peak:
                    peak = equity
                drawdown = peak - equity
                max_drawdown = max(max_drawdown, drawdown)
            return max_drawdown
            
        elif syntax_list['name'] == 'strategyMaxDrawdownPercent':
            equity_curve = []
            current_equity = args[0]['account']['initial_capital']
            for trade in args[0]['closed_trades']:
                current_equity += trade['profit']
                equity_curve.append(current_equity)
            
            max_drawdown_percent = 0
            peak = equity_curve[0]
            for equity in equity_curve:
                if equity > peak:
                    peak = equity
                drawdown_percent = ((peak - equity) / peak) * 100 if peak != 0 else 0
                max_drawdown_percent = max(max_drawdown_percent, drawdown_percent)
            return max_drawdown_percent
            
        elif syntax_list['name'] == 'strategyMaxRunup':
            equity_curve = []
            current_equity = args[0]['account']['initial_capital']
            for trade in args[0]['closed_trades']:
                current_equity += trade['profit']
                equity_curve.append(current_equity)
            
            max_runup = 0
            trough = equity_curve[0]
            for equity in equity_curve:
                if equity < trough:
                    trough = equity
                runup = equity - trough
                max_runup = max(max_runup, runup)
            return max_runup
            
        elif syntax_list['name'] == 'strategyMaxRunupPercent':
            equity_curve = []
            current_equity = args[0]['account']['initial_capital']
            for trade in args[0]['closed_trades']:
                current_equity += trade['profit']
                equity_curve.append(current_equity)
            
            max_runup_percent = 0
            trough = equity_curve[0]
            for equity in equity_curve:
                if equity < trough:
                    trough = equity
                runup_percent = ((equity - trough) / trough) * 100 if trough != 0 else 0
                max_runup_percent = max(max_runup_percent, runup_percent)
            return max_runup_percent

        elif syntax_list['name'] == 'strategyNetProfit':
            return sum(trade['profit'] for trade in args[0]['closed_trades'])
            
        elif syntax_list['name'] == 'strategyNetProfitPercent':
            initial_capital = args[0]['account']['initial_capital']
            net_profit = sum(trade['profit'] for trade in args[0]['closed_trades'])
            return (net_profit / initial_capital) * 100 if initial_capital != 0 else 0
            
        elif syntax_list['name'] == 'strategyOpenProfit':
            return sum(trade['unrealized_profit'] for trade in args[0]['open_trades'])
            
        elif syntax_list['name'] == 'strategyOpenProfitPercent':
            initial_capital = args[0]['account']['initial_capital']
            open_profit = sum(trade['unrealized_profit'] for trade in args[0]['open_trades'])
            return (open_profit / initial_capital) * 100 if initial_capital != 0 else 0
            
        elif syntax_list['name'] == 'strategyOpenTrades':
            return len(args[0]['open_trades'])
            
        elif syntax_list['name'] == 'strategyOpenTradesCapitalHeld':
            return sum(trade['margin_required'] for trade in args[0]['open_trades'])
            
        elif syntax_list['name'] == 'strategyPositionAvgPrice':
            open_positions = args[0]['open_trades']
            total_cost = sum(trade['entry_price'] * trade['contracts'] for trade in open_positions)
            total_contracts = sum(trade['contracts'] for trade in open_positions)
            return total_cost / total_contracts if total_contracts > 0 else 0
            
        elif syntax_list['name'] == 'strategyPositionEntryName':
            return args[0]['position']['entry_name'] if args[0]['position'] else ''
            
        elif syntax_list['name'] == 'strategyPositionSize':
            return sum(trade['contracts'] for trade in args[0]['open_trades'])
            
        elif syntax_list['name'] == 'strategyWinTrades':
            return sum(1 for trade in args[0]['closed_trades'] if trade['profit'] > 0)


        # timeframe is

        elif syntax_list['name'] == 'timeClose':
            bar_data = args[0]
            return bar_data['timestamp'] + bar_data['bar_length']
            
        elif syntax_list['name'] == 'timeTradingDay':
            bar_data = args[0]
            timestamp = bar_data['timestamp']
            day_start = timestamp - (timestamp % 86400)
            return day_start + bar_data['session_offset']
            
        elif syntax_list['name'] == 'timeframeIsDaily':
            timeframe_data = args[0]
            return timeframe_data['unit'] == 'day' and timeframe_data['value'] == 1
            
        elif syntax_list['name'] == 'timeframeIsDWM':
            timeframe_data = args[0]
            return timeframe_data['unit'] in ['day', 'week', 'month']
            
        elif syntax_list['name'] == 'timeframeIsIntraday':
            timeframe_data = args[0]
            return timeframe_data['unit'] in ['minute', 'second', 'tick']
            
        elif syntax_list['name'] == 'timeframeIsMinutes':
            timeframe_data = args[0]
            return timeframe_data['unit'] == 'minute'
            
        elif syntax_list['name'] == 'timeframeIsMonthly':
            timeframe_data = args[0]
            return timeframe_data['unit'] == 'month' and timeframe_data['value'] == 1
            
        elif syntax_list['name'] == 'timeframeIsSeconds':
            timeframe_data = args[0]
            return timeframe_data['unit'] == 'second'
            
        elif syntax_list['name'] == 'timeframeIsTicks':
            timeframe_data = args[0]
            return timeframe_data['unit'] == 'tick'
            
        elif syntax_list['name'] == 'timeframeIsWeekly':
            timeframe_data = args[0]
            return timeframe_data['unit'] == 'week' and timeframe_data['value'] == 1
            
        elif syntax_list['name'] == 'timeframeMainPeriod':
            timeframe_data = args[0]
            return timeframe_data['main_period']
            
        elif syntax_list['name'] == 'timeframeMultiplier':
            timeframe_data = args[0]
            return timeframe_data['value']
            
        elif syntax_list['name'] == 'timeframePeriod':
            timeframe_data = args[0]
            base_periods = {'tick': 1, 'second': 1, 'minute': 60, 'hour': 3600, 'day': 86400, 'week': 604800, 'month': 2592000}
            return base_periods[timeframe_data['unit']] * timeframe_data['value']
            
        elif syntax_list['name'] == 'timeNow':
            return int(time.time())
            
        elif syntax_list['name'] == 'weekOfYear':
            timestamp = args[0]
            days_since_epoch = timestamp // 86400
            day_of_year = days_since_epoch % 365.25
            return int((day_of_year + 10) // 7)
            
        elif syntax_list['name'] == 'year':
            timestamp = args[0]
            seconds_per_year = 31536000
            years_since_epoch = timestamp // seconds_per_year
            return 1970 + years_since_epoch


        # show style

        elif syntax_list['name'] == 'showStyleArea':
            style_data = {
                'type': 'plot_style',
                'style': 'area',
                'fill_opacity': 0.5 if not args else args[0]
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleAreaBr':
            style_data = {
                'type': 'plot_style',
                'style': 'area_br',
                'fill_opacity': 0.5 if not args else args[0],
                'break_gaps': True
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleCircles':
            style_data = {
                'type': 'plot_style',
                'style': 'circles',
                'radius': 3 if not args else args[0]
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleColumns':
            style_data = {
                'type': 'plot_style',
                'style': 'columns',
                'width': 0.8 if not args else args[0]
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleCross':
            style_data = {
                'type': 'plot_style',
                'style': 'cross',
                'size': 5 if not args else args[0]
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleHistogram':
            style_data = {
                'type': 'plot_style',
                'style': 'histogram',
                'base_level': 0 if not args else args[0]
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleLine':
            style_data = {
                'type': 'plot_style',
                'style': 'line',
                'width': 1 if not args else args[0]
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleLineBr':
            style_data = {
                'type': 'plot_style',
                'style': 'line_br',
                'width': 1 if not args else args[0],
                'break_gaps': True
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleStepLine':
            style_data = {
                'type': 'plot_style',
                'style': 'stepline',
                'width': 1 if not args else args[0]
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleStepLineDiamond':
            style_data = {
                'type': 'plot_style',
                'style': 'stepline_diamond',
                'width': 1 if not args else args[0],
                'marker_size': 5
            }
            return style_data
            
        elif syntax_list['name'] == 'showStyleStepLineBr':
            style_data = {
                'type': 'plot_style',
                'style': 'stepline_br',
                'width': 1 if not args else args[0],
                'break_gaps': True
            }
            return style_data
            
        elif syntax_list['name'] == 'positionBottomCenter':
            position_data = {
                'vertical': 'bottom',
                'horizontal': 'center',
                'alignment': 'bottom_center'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionBottomLeft':
            position_data = {
                'vertical': 'bottom',
                'horizontal': 'left',
                'alignment': 'bottom_left'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionBottomRight':
            position_data = {
                'vertical': 'bottom',
                'horizontal': 'right',
                'alignment': 'bottom_right'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionMiddleCenter':
            position_data = {
                'vertical': 'middle',
                'horizontal': 'center',
                'alignment': 'middle_center'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionMiddleLeft':
            position_data = {
                'vertical': 'middle',
                'horizontal': 'left',
                'alignment': 'middle_left'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionMiddleRight':
            position_data = {
                'vertical': 'middle',
                'horizontal': 'right',
                'alignment': 'middle_right'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionTopCenter':
            position_data = {
                'vertical': 'top',
                'horizontal': 'center',
                'alignment': 'top_center'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionTopLeft':
            position_data = {
                'vertical': 'top',
                'horizontal': 'left',
                'alignment': 'top_left'
            }
            return position_data
            
        elif syntax_list['name'] == 'positionTopRight':
            position_data = {
                'vertical': 'top',
                'horizontal': 'right',
                'alignment': 'top_right'
            }
            return position_data
            
        elif syntax_list['name'] == 'scaleLeft':
            scale_data = {
                'scale_position': 'left',
                'visible': True
            }
            return scale_data
            
        elif syntax_list['name'] == 'scaleNone':
            scale_data = {
                'scale_position': 'none',
                'visible': False
            }
            return scale_data
            
        elif syntax_list['name'] == 'scaleRight':
            scale_data = {
                'scale_position': 'right',
                'visible': True
            }
            return scale_data
            
        elif syntax_list['name'] == 'sessionExtended':
            session_data = {
                'session_type': 'extended',
                'include_pre_post': True,
                'extended_hours': True
            }
            return session_data
            
        elif syntax_list['name'] == 'sessionRegular':
            session_data = {
                'session_type': 'regular',
                'include_pre_post': False,
                'extended_hours': False
            }
            return session_data
            
        elif syntax_list['name'] == 'settlementAsCloseInherit':
            settlement_data = {
                'settlement_as_close': 'inherit',
                'use_settlement': None
            }
            return settlement_data
            
        elif syntax_list['name'] == 'settlementAsCloseOff':
            settlement_data = {
                'settlement_as_close': False,
                'use_settlement': False
            }
            return settlement_data
            
        elif syntax_list['name'] == 'settlementAsCloseOn':
            settlement_data = {
                'settlement_as_close': True,
                'use_settlement': True
            }
            return settlement_data


        # shape
        
        elif syntax_list['name'] == 'shapeArrowDown':
            return {
                'type': 'shape',
                'shape': 'arrow_down',
                'points': [[0, -1], [1, 0], [0.5, 0], [0.5, 1], [-0.5, 1], [-0.5, 0], [-1, 0]]
            }
            
        elif syntax_list['name'] == 'shapeArrowUp':
            return {
                'type': 'shape',
                'shape': 'arrow_up',
                'points': [[0, 1], [1, 0], [0.5, 0], [0.5, -1], [-0.5, -1], [-0.5, 0], [-1, 0]]
            }
            
        elif syntax_list['name'] == 'shapeCircle':
            return {
                'type': 'shape',
                'shape': 'circle',
                'radius': 1.0,
                'segments': 32
            }
            
        elif syntax_list['name'] == 'shapeCross':
            return {
                'type': 'shape',
                'shape': 'cross',
                'points': [[0.5, 0.5], [-0.5, -0.5], [0, 0], [-0.5, 0.5], [0.5, -0.5]]
            }
            
        elif syntax_list['name'] == 'shapeDiamond':
            return {
                'type': 'shape',
                'shape': 'diamond',
                'points': [[0, 1], [1, 0], [0, -1], [-1, 0]]
            }
            
        elif syntax_list['name'] == 'shapeFlag':
            return {
                'type': 'shape',
                'shape': 'flag',
                'points': [[0, 0], [0, 1], [1, 0.75], [0, 0.5]]
            }
            
        elif syntax_list['name'] == 'shapeLabelDown':
            return {
                'type': 'shape',
                'shape': 'label_down',
                'points': [[0, 0], [1, -1], [-1, -1]]
            }
            
        elif syntax_list['name'] == 'shapeLabelUp':
            return {
                'type': 'shape',
                'shape': 'label_up',
                'points': [[0, 0], [1, 1], [-1, 1]]
            }
            
        elif syntax_list['name'] == 'shapeSquare':
            return {
                'type': 'shape',
                'shape': 'square',
                'points': [[1, 1], [1, -1], [-1, -1], [-1, 1]]
            }
            
        elif syntax_list['name'] == 'shapeTriangleDown':
            return {
                'type': 'shape',
                'shape': 'triangle_down',
                'points': [[0, -1], [1, 1], [-1, 1]]
            }
            
        elif syntax_list['name'] == 'shapeTriangleUp':
            return {
                'type': 'shape',
                'shape': 'triangle_up',
                'points': [[0, 1], [1, -1], [-1, -1]]
            }
            
        elif syntax_list['name'] == 'shapeXCross':
            return {
                'type': 'shape',
                'shape': 'xcross',
                'points': [[1, 1], [-1, -1], [0, 0], [-1, 1], [1, -1]]
            }
            
        elif syntax_list['name'] == 'sizeAuto':
            return {
                'type': 'size',
                'value': 'auto',
                'scale_factor': 1.0
            }
            
        elif syntax_list['name'] == 'sizeHuge':
            return {
                'type': 'size',
                'value': 'huge',
                'scale_factor': 2.5
            }
            
        elif syntax_list['name'] == 'sizeLarge':
            return {
                'type': 'size',
                'value': 'large',
                'scale_factor': 1.5
            }
            
        elif syntax_list['name'] == 'sizeNormal':
            return {
                'type': 'size',
                'value': 'normal',
                'scale_factor': 1.0
            }
            
        elif syntax_list['name'] == 'sizeSmall':
            return {
                'type': 'size',
                'value': 'small',
                'scale_factor': 0.75
            }
            
        elif syntax_list['name'] == 'sizeTiny':
            return {
                'type': 'size',
                'value': 'tiny',
                'scale_factor': 0.5
            }
            
        elif syntax_list['name'] == 'splitsDenominator':
            return {
                'type': 'splits',
                'value': args[0]['denominator'] if args else 1,
                'split_type': 'denominator'
            }
            
        elif syntax_list['name'] == 'splitsNumerator':
            return {
                'type': 'splits',
                'value': args[0]['numerator'] if args else 1,
                'split_type': 'numerator'
            }



        elif syntax_list['name'] == 'strategyCash':
            return {
                'type': 'strategy_parameter',
                'parameter': 'cash',
                'value': args[0] if args else 100000
            }
            
        elif syntax_list['name'] == 'strategyCommissionCashPerContract':
            return {
                'type': 'strategy_parameter',
                'parameter': 'commission',
                'model': 'cash_per_contract',
                'value': args[0] if args else 0.0
            }
            
        elif syntax_list['name'] == 'strategyCommissionCashPerOrder':
            return {
                'type': 'strategy_parameter',
                'parameter': 'commission',
                'model': 'cash_per_order',
                'value': args[0] if args else 0.0
            }
            
        elif syntax_list['name'] == 'strategyCommissionPercent':
            return {
                'type': 'strategy_parameter',
                'parameter': 'commission',
                'model': 'percent',
                'value': args[0] if args else 0.0
            }
            
        elif syntax_list['name'] == 'strategyDirectionAll':
            return {
                'type': 'strategy_parameter',
                'parameter': 'direction',
                'value': 'all'
            }
            
        elif syntax_list['name'] == 'strategyDirectionLong':
            return {
                'type': 'strategy_parameter',
                'parameter': 'direction',
                'value': 'long'
            }
            
        elif syntax_list['name'] == 'strategyDirectionShort':
            return {
                'type': 'strategy_parameter',
                'parameter': 'direction',
                'value': 'short'
            }
            
        elif syntax_list['name'] == 'strategyFixed':
            return {
                'type': 'strategy_parameter',
                'parameter': 'position_size',
                'model': 'fixed',
                'value': args[0] if args else 1
            }
            
        elif syntax_list['name'] == 'strategyLong':
            return {
                'type': 'strategy_parameter',
                'parameter': 'position',
                'value': 'long'
            }
            
        elif syntax_list['name'] == 'strategyOcaCancel':
            return {
                'type': 'strategy_parameter',
                'parameter': 'oca',
                'behavior': 'cancel'
            }
            
        elif syntax_list['name'] == 'strategyOcaNone':
            return {
                'type': 'strategy_parameter',
                'parameter': 'oca',
                'behavior': 'none'
            }
            
        elif syntax_list['name'] == 'strategyOcaReduce':
            return {
                'type': 'strategy_parameter',
                'parameter': 'oca',
                'behavior': 'reduce'
            }
            
        elif syntax_list['name'] == 'strategyPercentOfEquity':
            return {
                'type': 'strategy_parameter',
                'parameter': 'position_size',
                'model': 'percent_of_equity',
                'value': args[0] if args else 100
            }
            
        elif syntax_list['name'] == 'strategyShort':
            return {
                'type': 'strategy_parameter',
                'parameter': 'position',
                'value': 'short'
            }
            
        elif syntax_list['name'] == 'textAlignBottom':
            return {
                'type': 'text_parameter',
                'parameter': 'vertical_align',
                'value': 'bottom'
            }
            
        elif syntax_list['name'] == 'textAlignCenter':
            return {
                'type': 'text_parameter',
                'parameter': 'horizontal_align',
                'value': 'center'
            }
            
        elif syntax_list['name'] == 'textAlignLeft':
            return {
                'type': 'text_parameter',
                'parameter': 'horizontal_align',
                'value': 'left'
            }
            
        elif syntax_list['name'] == 'textAlignRight':
            return {
                'type': 'text_parameter',
                'parameter': 'horizontal_align',
                'value': 'right'
            }
            
        elif syntax_list['name'] == 'textAlignTop':
            return {
                'type': 'text_parameter',
                'parameter': 'vertical_align',
                'value': 'top'
            }
            
        elif syntax_list['name'] == 'textWrapAuto':
            return {
                'type': 'text_parameter',
                'parameter': 'wrap',
                'value': 'auto'
            }
            
        elif syntax_list['name'] == 'textWrapNone':
            return {
                'type': 'text_parameter',
                'parameter': 'wrap',
                'value': 'none'
            }
            
        elif syntax_list['name'] == 'trueValue':
            return {
                'type': 'boolean',
                'value': True
            }


        elif syntax_list['name'] == 'locationAboveBar':
            return {
                'type': 'location',
                'position': 'above_bar',
                'offset': 1
            }
            
        elif syntax_list['name'] == 'locationAbsolute':
            return {
                'type': 'location',
                'position': 'absolute',
                'coordinates': args[0] if args else [0, 0]
            }
            
        elif syntax_list['name'] == 'locationBelowBar':
            return {
                'type': 'location',
                'position': 'below_bar',
                'offset': -1
            }
            
        elif syntax_list['name'] == 'locationBottom':
            return {
                'type': 'location',
                'position': 'bottom',
                'value': 0
            }
            
        elif syntax_list['name'] == 'locationTop':
            return {
                'type': 'location',
                'position': 'top',
                'value': 100
            }
            
        elif syntax_list['name'] == 'mathE':
            return {
                'type': 'constant',
                'name': 'e',
                'value': 2.718281828459045
            }
            
        elif syntax_list['name'] == 'mathPhi':
            return {
                'type': 'constant',
                'name': 'phi',
                'value': 1.618033988749895
            }
            
        elif syntax_list['name'] == 'mathPi':
            return {
                'type': 'constant',
                'name': 'pi',
                'value': 3.141592653589793
            }
            
        elif syntax_list['name'] == 'mathRPhi':
            return {
                'type': 'constant',
                'name': 'rphi',
                'value': 0.618033988749895
            }
            
        elif syntax_list['name'] == 'orderAscending':
            return {
                'type': 'order',
                'direction': 'ascending',
                'value': 1
            }
            
        elif syntax_list['name'] == 'orderDescending':
            return {
                'type': 'order',
                'direction': 'descending',
                'value': -1
            }
            
        elif syntax_list['name'] == 'onTick':
            return {
                'type': 'event',
                'trigger': 'tick',
                'timestamp': args[0] if args else 0
            }
            
        elif syntax_list['name'] == 'onBar':
            return {
                'type': 'event',
                'trigger': 'bar',
                'timestamp': args[0] if args else 0
            }
            
        elif syntax_list['name'] == '=':
            return {
                'type': 'operator',
                'operation': 'assign',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '+':
            return {
                'type': 'operator',
                'operation': 'add',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '-':
            return {
                'type': 'operator',
                'operation': 'subtract',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '*':
            return {
                'type': 'operator',
                'operation': 'multiply',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '/':
            return {
                'type': 'operator',
                'operation': 'divide',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '%':
            return {
                'type': 'operator',
                'operation': 'modulo',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '==':
            return {
                'type': 'operator',
                'operation': 'equal',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '!=':
            return {
                'type': 'operator',
                'operation': 'not_equal',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '>':
            return {
                'type': 'operator',
                'operation': 'greater',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '<':
            return {
                'type': 'operator',
                'operation': 'less',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '>=':
            return {
                'type': 'operator',
                'operation': 'greater_equal',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == '<=':
            return {
                'type': 'operator',
                'operation': 'less_equal',
                'left': args[0],
                'right': args[1]
            }

        elif syntax_list['name'] == 'and':
            return {
                'type': 'logical',
                'operation': 'and',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == 'or':
            return {
                'type': 'logical',
                'operation': 'or',
                'left': args[0],
                'right': args[1]
            }
            
        elif syntax_list['name'] == 'not':
            return {
                'type': 'logical',
                'operation': 'not',
                'operand': args[0]
            }
            
        elif syntax_list['name'] == 'if':
            return {
                'type': 'control',
                'operation': 'if',
                'condition': args[0],
                'then': args[1],
                'else': args[2] if len(args) > 2 else None
            }
            
        elif syntax_list['name'] == 'else':
            return {
                'type': 'control',
                'operation': 'else',
                'body': args[0]
            }
            
        elif syntax_list['name'] == 'for':
            return {
                'type': 'control',
                'operation': 'for',
                'init': args[0],
                'condition': args[1],
                'increment': args[2],
                'body': args[3]
            }
            
        elif syntax_list['name'] == 'while':
            return {
                'type': 'control',
                'operation': 'while',
                'condition': args[0],
                'body': args[1]
            }
            
        elif syntax_list['name'] == 'let':
            return {
                'type': 'declaration',
                'operation': 'let',
                'name': args[0],
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'arr':
            return {
                'type': 'array',
                'elements': args[0] if args else []
            }
            
        elif syntax_list['name'] == 'bool':
            return {
                'type': 'boolean',
                'value': bool(args[0]) if args else False
            }
            
        elif syntax_list['name'] == 'box':
            return {
                'type': 'box',
                'left': args[0] if args else 0,
                'top': args[1] if len(args) > 1 else 0,
                'right': args[2] if len(args) > 2 else 0,
                'bottom': args[3] if len(args) > 3 else 0
            }
            
        elif syntax_list['name'] == 'chartPoint':
            return {
                'type': 'chart_point',
                'x': args[0] if args else 0,
                'y': args[1] if len(args) > 1 else 0
            }
            
        elif syntax_list['name'] == 'col':
            return {
                'type': 'color',
                'r': args[0] if args else 0,
                'g': args[1] if len(args) > 1 else 0,
                'b': args[2] if len(args) > 2 else 0
            }
            
        elif syntax_list['name'] == 'const':
            return {
                'type': 'constant',
                'name': args[0],
                'value': args[1]
            }
            
        elif syntax_list['name'] == 'float':
            return {
                'type': 'float',
                'value': float(args[0]) if args else 0.0
            }
            
        elif syntax_list['name'] == 'int':
            return {
                'type': 'integer',
                'value': int(args[0]) if args else 0
            }
            
        elif syntax_list['name'] == 'label':
            return {
                'type': 'label',
                'text': args[0] if args else '',
                'x': args[1] if len(args) > 1 else 0,
                'y': args[2] if len(args) > 2 else 0
            }

        elif syntax_list['name'] == 'dayOfMonth':
            return {
                'type': 'time',
                'component': 'day_of_month',
                'value': args[0]['timestamp'].day if args else 1
            }
            
        elif syntax_list['name'] == 'dayOfWeek':
            return {
                'type': 'time',
                'component': 'day_of_week',
                'value': args[0]['timestamp'].weekday() if args else 0
            }
            
        elif syntax_list['name'] == 'hour':
            return {
                'type': 'time',
                'component': 'hour',
                'value': args[0]['timestamp'].hour if args else 0
            }
            
        elif syntax_list['name'] == 'minute':
            return {
                'type': 'time',
                'component': 'minute',
                'value': args[0]['timestamp'].minute if args else 0
            }
            
        elif syntax_list['name'] == 'month':
            return {
                'type': 'time',
                'component': 'month',
                'value': args[0]['timestamp'].month if args else 1
            }
            
        elif syntax_list['name'] == 'second':
            return {
                'type': 'time',
                'component': 'second',
                'value': args[0]['timestamp'].second if args else 0
            }
            
        elif syntax_list['name'] == 'time':
            return {
                'type': 'time',
                'component': 'timestamp',
                'value': args[0]['timestamp'].timestamp() if args else 0
            }
            
        elif syntax_list['name'] == 'timeClose':
            return {
                'type': 'time',
                'component': 'close_time',
                'value': args[0]['bar_close_time'] if args else 0
            }
            
        elif syntax_list['name'] == 'timeTradingDay':
            return {
                'type': 'time',
                'component': 'trading_day',
                'value': args[0]['trading_day_timestamp'] if args else 0
            }
            
        elif syntax_list['name'] == 'timeNow':
            return {
                'type': 'time',
                'component': 'current_time',
                'value': int(time.time())
            }
            
        elif syntax_list['name'] == 'weekOfYear':
            return {
                'type': 'time',
                'component': 'week_of_year',
                'value': args[0]['timestamp'].isocalendar()[1] if args else 1
            }
            
        elif syntax_list['name'] == 'year':
            return {
                'type': 'time',
                'component': 'year',
                'value': args[0]['timestamp'].year if args else 1970
            }
            
        elif syntax_list['name'] == 'sessionIsFirstBar':
            return {
                'type': 'session',
                'component': 'first_bar',
                'value': args[0]['session']['is_first_bar'] if args else False
            }
            
        elif syntax_list['name'] == 'sessionIsFirstBarRegular':
            return {
                'type': 'session',
                'component': 'first_bar_regular',
                'value': args[0]['session']['is_first_bar_regular'] if args else False
            }
            
        elif syntax_list['name'] == 'sessionIsLastBar':
            return {
                'type': 'session',
                'component': 'last_bar',
                'value': args[0]['session']['is_last_bar'] if args else False
            }
            
        elif syntax_list['name'] == 'sessionIsLastBarRegular':
            return {
                'type': 'session',
                'component': 'last_bar_regular',
                'value': args[0]['session']['is_last_bar_regular'] if args else False
            }
            
        elif syntax_list['name'] == 'sessionIsMarket':
            return {
                'type': 'session',
                'component': 'is_market',
                'value': args[0]['session']['is_market'] if args else False
            }
            
        elif syntax_list['name'] == 'sessionIsPostMarket':
            return {
                'type': 'session',
                'component': 'is_post_market',
                'value': args[0]['session']['is_post_market'] if args else False
            }
            
        elif syntax_list['name'] == 'sessionIsPreMarket':
            return {
                'type': 'session',
                'component': 'is_pre_market',
                'value': args[0]['session']['is_pre_market'] if args else False
            }


        # table 

        elif syntax_list['name'] == 'tableFunc':
            return {
                'type': 'table',
                'operation': 'create',
                'id': args[0] if args else 'default_table',
                'rows': 1,
                'columns': 1
            }
            
        elif syntax_list['name'] == 'tableCellFunc':
            return {
                'type': 'table',
                'operation': 'get_cell',
                'table_id': args[0],
                'row': args[1],
                'column': args[2]
            }
            
        elif syntax_list['name'] == 'tableCellSetBgColFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_bgcolor',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'color': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetHeightFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_height',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'height': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetTextFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_text',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'text': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetTextColFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_text_color',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'color': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetTextFontFamily':
            return {
                'type': 'table',
                'operation': 'set_cell_font_family',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'font_family': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetTextHAlignFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_text_halign',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'alignment': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetTextSizeFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_text_size',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'size': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetTextVAlignFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_text_valign',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'alignment': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetToolTipFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_tooltip',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'tooltip': args[3]
            }
            
        elif syntax_list['name'] == 'tableCellSetWidthFunc':
            return {
                'type': 'table',
                'operation': 'set_cell_width',
                'table_id': args[0],
                'row': args[1],
                'column': args[2],
                'width': args[3]
            }
            
        elif syntax_list['name'] == 'tableClearFunc':
            return {
                'type': 'table',
                'operation': 'clear',
                'table_id': args[0]
            }
            
        elif syntax_list['name'] == 'tableDeleteFunc':
            return {
                'type': 'table',
                'operation': 'delete',
                'table_id': args[0]
            }
            
        elif syntax_list['name'] == 'tableMergeCellsFunc':
            return {
                'type': 'table',
                'operation': 'merge_cells',
                'table_id': args[0],
                'start_row': args[1],
                'start_col': args[2],
                'end_row': args[3],
                'end_col': args[4]
            }
            
        elif syntax_list['name'] == 'tableNewFunc':
            return {
                'type': 'table',
                'operation': 'new',
                'id': args[0],
                'rows': args[1],
                'columns': args[2]
            }
            
        elif syntax_list['name'] == 'tableSetBgColFunc':
            return {
                'type': 'table',
                'operation': 'set_bgcolor',
                'table_id': args[0],
                'color': args[1]
            }
            
        elif syntax_list['name'] == 'tableSetBorderColFunc':
            return {
                'type': 'table',
                'operation': 'set_border_color',
                'table_id': args[0],
                'color': args[1]
            }
            
        elif syntax_list['name'] == 'tableSetBorderWidthFunc':
            return {
                'type': 'table',
                'operation': 'set_border_width',
                'table_id': args[0],
                'width': args[1]
            }
            
        elif syntax_list['name'] == 'tableSetFrameColFunc':
            return {
                'type': 'table',
                'operation': 'set_frame_color',
                'table_id': args[0],
                'color': args[1]
            }
            
        elif syntax_list['name'] == 'tableSetFrameWidthFunc':
            return {
                'type': 'table',
                'operation': 'set_frame_width',
                'table_id': args[0],
                'width': args[1]
            }
            
        elif syntax_list['name'] == 'tableSetPositionFunc':
            return {
                'type': 'table',
                'operation': 'set_position',
                'table_id': args[0],
                'position': args[1]
            }


"""-----------------------------------------------------------------------------------------------------------------"""

# Evaluator

class Evaluator:
    def __init__(self, ast):
        self.ast = ast
        self.environment = {}

    def evaluate(self):
        return self._evaluate(self.ast)


"""-----------------------------------------------------------------------------------------------------------------"""

#registries


def _initialize_registries(self):
    registry = {
        'syntax_registry': {
            'type': 'syntax_evaluation',
            'elements': {
                # SECTION 1: BASIC PRICE DATA
                'open': {'type': 'price_data', 'params': {}},  # single-line format
                'high': {'type': 'price_data', 'params': {}},  # single-line format
                'low': {'type': 'price_data', 'params': {}},  # single-line format
                'close': {'type': 'price_data', 'params': {}},  # single-line format
                'volume': {'type': 'price_data', 'params': {}},  # single-line format
                'hl2': {'type': 'price_data', 'params': {}},  # single-line format
                'hlc3': {'type': 'price_data', 'params': {}},  # single-line format
                'hlcc4': {'type': 'price_data', 'params': {}},  # single-line format
                'ohlc4': {'type': 'price_data', 'params': {}},  # single-line format

                # SECTION 2: BASIC PLOTTING FUNCTIONS
                'show': {
                    'type': 'plotting',
                    'params': {
                        'series': {'type': 'series', 'required': True},
                        'title': {'type': 'string', 'default': ''},
                        'color': {'type': 'color', 'default': 'auto'},
                        'linewidth': {'type': 'integer', 'default': 1},
                        'style': {'type': 'plotstyle', 'default': 'line'},
                        'trackprice': {'type': 'bool', 'default': False},
                        'histbase': {'type': 'integer', 'default': 0},
                        'offset': {'type': 'integer', 'default': 0},
                        'join': {'type': 'bool', 'default': False},
                        'editable': {'type': 'bool', 'default': True},
                        'show_last': {'type': 'integer', 'default': 0},
                        'display': {'type': 'display_type', 'default': 'all'},
                        'format': {'type': 'format_type', 'default': 'inherit'},
                        'precision': {'type': 'integer', 'default': 4},
                        'force_overlay': {'type': 'bool', 'default': False}
                    }
                },
                'showshape': {
                    'type': 'plotting',
                    'params': {
                        'series': {'type': 'series', 'required': True},
                        'title': {'type': 'string', 'default': ''},
                        'location': {'type': 'string', 'default': 'abovebar'},
                        'color': {'type': 'color', 'default': 'blue'},
                        'style': {'type': 'string', 'default': 'circle'},
                        'size': {'type': 'string', 'default': 'auto'},
                        'text': {'type': 'string', 'default': ''},
                        'textcolor': {'type': 'color', 'default': 'black'},
                        'editable': {'type': 'bool', 'default': True}
                    }
                },
                'showcond': {
                    'type': 'plotting',
                    'params': {
                        'condition': {'type': 'series', 'required': True},
                        'title': {'type': 'string', 'default': ''},
                        'color': {'type': 'color', 'default': 'blue'},
                        'style': {'type': 'string', 'default': 'line'},
                        'linewidth': {'type': 'integer', 'default': 1}
                    }
                },

                'showcond': {
                    'type': 'visualization',
                    'params': {
                        'condition': {'type': 'series', 'required': True},
                        'title': {'type': 'string', 'optional': True},
                        'color': {'type': 'color', 'optional': True},
                        'style': {'type': 'enum', 'values': ['line', 'stepline', 'histogram', 'circles', 'cross', 'area', 'columns'], 'default': 'line'},
                        'linewidth': {'type': 'integer', 'default': 1},
                        'display': {'type': 'enum', 'values': ['all', 'none'], 'default': 'all'}
                    }
                },
                'showStyleLine': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleStepLine': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleHistogram': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleCircles': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleCross': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleArea': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleColumns': {'type': 'style_constant', 'params': {}},  # single-line format

                'showStyleAreaBr': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleLineBr': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleStepLineBr': {'type': 'style_constant', 'params': {}},  # single-line format
                'showStyleStepLineDiamond': {'type': 'style_constant', 'params': {}},  # single-line format
                'positionTopLeft': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionTopCenter': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionTopRight': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionMiddleLeft': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionMiddleCenter': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionMiddleRight': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionBottomLeft': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionBottomCenter': {'type': 'position_constant', 'params': {}},  # single-line format
                'positionBottomRight': {'type': 'position_constant', 'params': {}},  # single-line format

                'scaleLeft': {'type': 'visualization', 'params': {}},  # single-line format
                'scaleRight': {'type': 'visualization', 'params': {}},  # single-line format
                'scaleNone': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeArrowUp': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeArrowDown': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeCircle': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeCross': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeDiamond': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeFlag': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeLabelUp': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeLabelDown': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeSquare': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeTriangleUp': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeTriangleDown': {'type': 'visualization', 'params': {}},  # single-line format
                'shapeXCross': {'type': 'visualization', 'params': {}},  # single-line format

                'sizeAuto': {'type': 'visualization', 'params': {}},  # single-line format
                'sizeHuge': {'type': 'visualization', 'params': {}},  # single-line format
                'sizeLarge': {'type': 'visualization', 'params': {}},  # single-line format
                'sizeNormal': {'type': 'visualization', 'params': {}},  # single-line format
                'sizeSmall': {'type': 'visualization', 'params': {}},  # single-line format
                'sizeTiny': {'type': 'visualization', 'params': {}},  # single-line format
                'textAlignCenter': {'type': 'visualization', 'params': {}},  # single-line format
                'textAlignLeft': {'type': 'visualization', 'params': {}},  # single-line format
                'textAlignRight': {'type': 'visualization', 'params': {}},  # single-line format
                'textAlignTop': {'type': 'visualization', 'params': {}},  # single-line format
                'textAlignBottom': {'type': 'visualization', 'params': {}},  # single-line format
                'textWrapAuto': {'type': 'visualization', 'params': {}},  # single-line format
                'textWrapNone': {'type': 'visualization', 'params': {}},  # single-line format

                'lineStyleSolid': {'type': 'visualization', 'params': {}},  # single-line format
                'lineStyleDashed': {'type': 'visualization', 'params': {}},  # single-line format
                'lineStyleDotted': {'type': 'visualization', 'params': {}},  # single-line format
                'lineStyleArrowLeft': {'type': 'visualization', 'params': {}},  # single-line format
                'lineStyleArrowRight': {'type': 'visualization', 'params': {}},  # single-line format
                'lineStyleArrowBoth': {'type': 'visualization', 'params': {}},  # single-line format
                'locationAboveBar': {'type': 'visualization', 'params': {}},  # single-line format
                'locationBelowBar': {'type': 'visualization', 'params': {}},  # single-line format
                'locationTop': {'type': 'visualization', 'params': {}},  # single-line format
                'locationBottom': {'type': 'visualization', 'params': {}},  # single-line format
                'locationAbsolute': {'type': 'visualization', 'params': {}},  # single-line format
                'extendNone': {'type': 'visualization', 'params': {}},  # single-line format
                'extendLeft': {'type': 'visualization', 'params': {}},  # single-line format
                'extendRight': {'type': 'visualization', 'params': {}},  # single-line format
                'extendBoth': {'type': 'visualization', 'params': {}},  # single-line format

                'labelStyleNone': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleLabel': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleArrowUp': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleArrowDown': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleCircle': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleSquare': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleDiamond': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleTriangleUp': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleTriangleDown': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleFlag': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleXCross': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleCross': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleText': {'type': 'visualization', 'params': {}},  # single-line format
                'labelStyleTextOutline': {'type': 'visualization', 'params': {}},  # single-line format

                'displayPane': {'type': 'visualization', 'params': {}},  # single-line format
                'displayPriceScale': {'type': 'visualization', 'params': {}},  # single-line format
                'hlineStyleSolid': {'type': 'visualization', 'params': {}},  # single-line format
                'hlineStyleDashed': {'type': 'visualization', 'params': {}},  # single-line format
                'hlineStyleDotted': {'type': 'visualization', 'params': {}},  # single-line format
                'yLocPrice': {'type': 'visualization', 'params': {}},  # single-line format
                'yLocAboveBar': {'type': 'visualization', 'params': {}},  # single-line format
                'yLocBelowBar': {'type': 'visualization', 'params': {}},  # single-line format
                'xLocBarIndex': {'type': 'visualization', 'params': {}},  # single-line format
                'xLocBarTime': {'type': 'visualization', 'params': {}},  # single-line format
                'fontFamilyDefault': {'type': 'visualization', 'params': {}},  # single-line format
                'fontFamilyMonospace': {'type': 'visualization', 'params': {}},  # single-line format

                # SECTION 3: TECHNICAL INDICATORS
                'taAccDist': {'type': 'indicator', 'params': {'high': {'type': 'series', 'default': 'high'}, 'low': {'type': 'series', 'default': 'low'}, 'close': {'type': 'series', 'default': 'close'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format
                'taAlma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 9}, 'offset': {'type': 'float', 'default': 0.85}, 'sigma': {'type': 'float', 'default': 6}}},  # single-line format
                'taAtr': {'type': 'indicator', 'params': {'length': {'type': 'integer', 'default': 14}}},  # single-line format
                'taBarsSince': {'type': 'indicator', 'params': {'condition': {'type': 'series', 'required': True}}},  # single-line format
                'taBb': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}, 'mult': {'type': 'float', 'default': 2}}},  # single-line format
                'taBbw': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}, 'mult': {'type': 'float', 'default': 2}}},  # single-line format
                'taCci': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'hlc3'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taChange': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}}},  # single-line format
                'taCmo': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 9}}},  # single-line format
                'taCog': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 10}}},  # single-line format
                'taCorrelation': {'type': 'indicator', 'params': {'source1': {'type': 'series', 'required': True}, 'source2': {'type': 'series', 'required': True}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format

                'taCross': {'type': 'indicator', 'params': {'source1': {'type': 'series', 'required': True}, 'source2': {'type': 'series', 'required': True}}},  # single-line format
                'taCrossover': {'type': 'indicator', 'params': {'source1': {'type': 'series', 'required': True}, 'source2': {'type': 'series', 'required': True}}},  # single-line format
                'taCrossunder': {'type': 'indicator', 'params': {'source1': {'type': 'series', 'required': True}, 'source2': {'type': 'series', 'required': True}}},  # single-line format
                'taCum': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}}},  # single-line format
                'taDev': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taDmi': {'type': 'indicator', 'params': {'length': {'type': 'integer', 'default': 14}, 'smoothing': {'type': 'integer', 'default': 14}}},  # single-line format
                'taEma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 9}}},  # single-line format
                'taFalling': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 1}}},  # single-line format
                'taHighest': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'high'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format

                'taHighestBars': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'high'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taHma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 9}}},  # single-line format
                'taKc': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}, 'mult': {'type': 'float', 'default': 2}}},  # single-line format
                'taKcw': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}, 'mult': {'type': 'float', 'default': 2}}},  # single-line format
                'taLinReg': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 14}}},  # single-line format
                'taLowest': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'low'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taLowestBars': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'low'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taMacd': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'fastLength': {'type': 'integer', 'default': 12}, 'slowLength': {'type': 'integer', 'default': 26}, 'signalLength': {'type': 'integer', 'default': 9}}},  # single-line format
                'taMax': {'type': 'indicator', 'params': {'source1': {'type': 'series', 'required': True}, 'source2': {'type': 'series', 'required': True}}},  # single-line format
                'taMedian': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taMfi': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'hlc3'}, 'length': {'type': 'integer', 'default': 14}}},  # single-line format
                'taMin': {'type': 'indicator', 'params': {'source1': {'type': 'series', 'required': True}, 'source2': {'type': 'series', 'required': True}}},  # single-line format
                'taMode': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format

                'taMom': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 10}}},  # single-line format
                'taPercentile': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}, 'percentage': {'type': 'float', 'default': 50}}},  # single-line format
                'taPercentRank': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taPivotHigh': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'high'}, 'leftbars': {'type': 'integer', 'default': 5}, 'rightbars': {'type': 'integer', 'default': 5}}},  # single-line format
                'taPivotLow': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'low'}, 'leftbars': {'type': 'integer', 'default': 5}, 'rightbars': {'type': 'integer', 'default': 5}}},  # single-line format
                'taRange': {'type': 'indicator', 'params': {'length': {'type': 'integer', 'default': 14}}},  # single-line format
                'taRising': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 1}}},  # single-line format
                'taRma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 14}}},  # single-line format
                'taRoc': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 12}}},  # single-line format
                'taRsi': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 14}}},  # single-line format
                'taSar': {'type': 'indicator', 'params': {'start': {'type': 'float', 'default': 0.02}, 'increment': {'type': 'float', 'default': 0.02}, 'maximum': {'type': 'float', 'default': 0.2}}},  # single-line format
                'taSma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 9}}},  # single-line format

                'taStdev': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taStoch': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'high': {'type': 'series', 'default': 'high'}, 'low': {'type': 'series', 'default': 'low'}, 'length': {'type': 'integer', 'default': 14}, 'smoothK': {'type': 'integer', 'default': 3}, 'smoothD': {'type': 'integer', 'default': 3}}},  # single-line format
                'taSuperTrend': {'type': 'indicator', 'params': {'factor': {'type': 'float', 'default': 3}, 'atrPeriod': {'type': 'integer', 'default': 10}}},  # single-line format
                'taSwma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}}},  # single-line format
                'taTR': {'type': 'indicator', 'params': {'high': {'type': 'series', 'default': 'high'}, 'low': {'type': 'series', 'default': 'low'}, 'close': {'type': 'series', 'default': 'close'}}},  # single-line format
                'taTsi': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'shortLength': {'type': 'integer', 'default': 25}, 'longLength': {'type': 'integer', 'default': 13}, 'signalLength': {'type': 'integer', 'default': 13}}},  # single-line format
                'taValueWhen': {'type': 'indicator', 'params': {'condition': {'type': 'series', 'required': True}, 'source': {'type': 'series', 'required': True}, 'occurrence': {'type': 'integer', 'default': 0}}},  # single-line format
                'taVariance': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taVwap': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'hlc3'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format
                'taVwma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'volume': {'type': 'series', 'default': 'volume'}, 'length': {'type': 'integer', 'default': 20}}},  # single-line format
                'taWma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 9}}},  # single-line format
                'taWpr': {'type': 'indicator', 'params': {'length': {'type': 'integer', 'default': 14}}},  # single-line format

                'taVWAP': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'hlc3'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format
                'taWAD': {'type': 'indicator', 'params': {'high': {'type': 'series', 'default': 'high'}, 'low': {'type': 'series', 'default': 'low'}, 'close': {'type': 'series', 'default': 'close'}}},  # single-line format
                'taWVAD': {'type': 'indicator', 'params': {'high': {'type': 'series', 'default': 'high'}, 'low': {'type': 'series', 'default': 'low'}, 'close': {'type': 'series', 'default': 'close'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format
                'taIII': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'length': {'type': 'integer', 'default': 14}}},  # single-line format
                'taNVI': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format
                'taOBV': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format
                'taPVI': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format
                'taPVT': {'type': 'indicator', 'params': {'source': {'type': 'series', 'default': 'close'}, 'volume': {'type': 'series', 'default': 'volume'}}},  # single-line format

                # SECTION: STRATEGY FUNCTIONS
                'strategyAccountCurrency': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyAvgLosingTrade': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyAvgLosingTradePercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyAvgTrade': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyAvgTradePercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyAvgWinningTrade': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyAvgWinningTradePercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTrades': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesFirstIndex': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyEquity': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyEntry': {'type': 'strategy', 'params': {'id': {'type': 'string', 'required': True}, 'direction': {'type': 'string', 'required': True}, 'qty': {'type': 'float', 'default': 1.0}, 'limit': {'type': 'float', 'optional': True}, 'stop': {'type': 'float', 'optional': True}, 'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}}},  # single-line format
                'strategyExit': {'type': 'strategy', 'params': {'id': {'type': 'string', 'required': True}, 'from_entry': {'type': 'string', 'required': True}, 'qty': {'type': 'float', 'default': 'all'}, 'limit': {'type': 'float', 'optional': True}, 'stop': {'type': 'float', 'optional': True}, 'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}}},  # single-line format

                'strategyClose': {'type': 'strategy', 'params': {'id': {'type': 'string', 'required': True}, 'when': {'type': 'series', 'default': True}, 'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}}},  # single-line format
                'strategyCloseAll': {'type': 'strategy', 'params': {'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}}},  # single-line format
                'strategyEvenTrades': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyGrossLoss': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyGrossLossPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyGrossProfit': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyGrossProfitPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyInitialCapital': {'type': 'strategy', 'params': {'value': {'type': 'float', 'default': 100000}}},  # single-line format
                'strategyLossTrades': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyMarginLiquidationPrice': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyMaxContractsHeldAll': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyMaxContractsHeldLong': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyMaxContractsHeldShort': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyMaxDrawdown': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyMaxDrawdownPercent': {'type': 'strategy', 'params': {}},  # single-line format

                'strategyMaxRunup': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyMaxRunupPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyNetProfit': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyNetProfitPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenProfit': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenProfitPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTrades': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesCapitalHeld': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyPositionAvgPrice': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyPositionEntryName': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyPositionSize': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyWinTrades': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyCash': {'type': 'strategy', 'params': {'value': {'type': 'float', 'default': 100000}}},  # single-line format
                'strategyCommissionCashPerContract': {'type': 'strategy', 'params': {'value': {'type': 'float', 'default': 0}}},  # single-line format
                'strategyCommissionCashPerOrder': {'type': 'strategy', 'params': {'value': {'type': 'float', 'default': 0}}},  # single-line format
                'strategyCommissionPercent': {'type': 'strategy', 'params': {'value': {'type': 'float', 'default': 0}}},  # single-line format

                'strategyDirectionAll': {'type': 'strategy', 'params': {'value': {'type': 'string', 'default': 'all'}}},  # single-line format
                'strategyDirectionLong': {'type': 'strategy', 'params': {'value': {'type': 'string', 'default': 'long'}}},  # single-line format
                'strategyDirectionShort': {'type': 'strategy', 'params': {'value': {'type': 'string', 'default': 'short'}}},  # single-line format
                'strategyFixed': {'type': 'strategy', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'strategyLong': {'type': 'strategy', 'params': {'qty': {'type': 'float', 'default': 1.0}, 'limit': {'type': 'float', 'optional': True}, 'stop': {'type': 'float', 'optional': True}, 'oca_name': {'type': 'string', 'optional': True}, 'oca_type': {'type': 'string', 'default': 'none'}, 'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}}},  # single-line format
                'strategyOcaCancel': {'type': 'strategy', 'params': {'value': {'type': 'string', 'default': 'cancel'}}},  # single-line format
                'strategyOcaNone': {'type': 'strategy', 'params': {'value': {'type': 'string', 'default': 'none'}}},  # single-line format
                'strategyOcaReduce': {'type': 'strategy', 'params': {'value': {'type': 'string', 'default': 'reduce'}}},  # single-line format
                'strategyPercentOfEquity': {'type': 'strategy', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'strategyShort': {'type': 'strategy', 'params': {'qty': {'type': 'float', 'default': 1.0}, 'limit': {'type': 'float', 'optional': True}, 'stop': {'type': 'float', 'optional': True}, 'oca_name': {'type': 'string', 'optional': True}, 'oca_type': {'type': 'string', 'default': 'none'}, 'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}}},  # single-line format

                'strategyRiskAllowEntryIn': {'type': 'strategy_risk', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'strategyRiskMaxConsLossDays': {'type': 'strategy_risk', 'params': {'value': {'type': 'integer', 'required': True}}},  # single-line format
                'strategyRiskMaxDrawdown': {'type': 'strategy_risk', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'strategyRiskMaxIntradayFilledOrders': {'type': 'strategy_risk', 'params': {'value': {'type': 'integer', 'required': True}}},  # single-line format
                'strategyRiskMaxIntradayLoss': {'type': 'strategy_risk', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'strategyRiskMaxPositionSize': {'type': 'strategy_risk', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'strategyClosedTradesCommission': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesEntryBarIndex': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesEntryComment': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesEntryId': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesEntryPrice': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesEntryTime': {'type': 'strategy', 'params': {}},  # single-line format

                'strategyClosedTradesExitBarIndex': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesExitComment': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesExitId': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesExitPrice': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesExitTime': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesMaxDrawdown': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesMaxDrawdownPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesMaxRunup': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesMaxRunupPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesProfit': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesProfitPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyClosedTradesSize': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyConvertToAccount': {'type': 'strategy_conversion', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'strategyConvertToSymbol': {'type': 'strategy_conversion', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format

                'strategyDefaultEntryQty': {'type': 'strategy', 'params': {'value': {'type': 'float', 'default': 1.0}}},  # single-line format
                'strategyOpenTradesCommission': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesEntryBarIndex': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesEntryComment': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesEntryId': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesEntryPrice': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesEntryTime': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesMaxDrawdown': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesMaxDrawdownPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesMaxRunup': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesMaxRunupPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesProfit': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesProfitPercent': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyOpenTradesSize': {'type': 'strategy', 'params': {}},  # single-line format

                'strategyOrder': {'type': 'strategy', 'params': {'id': {'type': 'string', 'required': True}, 'direction': {'type': 'string', 'required': True}, 'qty': {'type': 'float', 'default': 1.0}, 'limit': {'type': 'float', 'optional': True}, 'stop': {'type': 'float', 'optional': True}, 'oca_name': {'type': 'string', 'optional': True}, 'oca_type': {'type': 'string', 'default': 'none'}, 'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}, 'cancel': {'type': 'series', 'optional': True}}},  # single-line format
                'strategyCancelAll': {'type': 'strategy', 'params': {'comment': {'type': 'string', 'optional': True}}},  # single-line format
                'strategyCancel': {'type': 'strategy', 'params': {'id': {'type': 'string', 'required': True}, 'comment': {'type': 'string', 'optional': True}}},  # single-line format
                'strategyClosePosition': {'type': 'strategy', 'params': {'comment': {'type': 'string', 'optional': True}, 'alert': {'type': 'bool', 'default': True}, 'immediately': {'type': 'bool', 'default': False}}},  # single-line format
                'strategyEntryPrice': {'type': 'strategy', 'params': {}},  # single-line format
                'strategyExitPrice': {'type': 'strategy', 'params': {}},  # single-line format

                # SECTION: TIME FUNCTIONS AND PROPERTIES
                'time': {'type': 'time', 'params': {'timezone': {'type': 'string', 'optional': True}}},  # single-line format
                'timeNow': {'type': 'time', 'params': {}},  # single-line format
                'timeClose': {'type': 'time', 'params': {}},  # single-line format
                'timeTradingDay': {'type': 'time', 'params': {}},  # single-line format
                'year': {'type': 'time', 'params': {}},  # single-line format
                'month': {'type': 'time', 'params': {}},  # single-line format
                'weekOfYear': {'type': 'time', 'params': {}},  # single-line format
                'dayOfMonth': {'type': 'time', 'params': {}},  # single-line format
                'dayOfWeek': {'type': 'time', 'params': {}},  # single-line format
                'hour': {'type': 'time', 'params': {}},  # single-line format
                'minute': {'type': 'time', 'params': {}},  # single-line format
                'second': {'type': 'time', 'params': {}},  # single-line format

                'timeframe': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsDaily': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsDWM': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsIntraday': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsMinutes': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsMonthly': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsSeconds': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsTicks': {'type': 'time', 'params': {}},  # single-line format
                'timeframeIsWeekly': {'type': 'time', 'params': {}},  # single-line format
                'timeframeMainPeriod': {'type': 'time', 'params': {}},  # single-line format
                'timeframeMultiplier': {'type': 'time', 'params': {}},  # single-line format
                'timeframePeriod': {'type': 'time', 'params': {}},  # single-line format

                'sessionIsFirstBar': {'type': 'session', 'params': {}},  # single-line format
                'sessionIsFirstBarRegular': {'type': 'session', 'params': {}},  # single-line format
                'sessionIsLastBar': {'type': 'session', 'params': {}},  # single-line format
                'sessionIsLastBarRegular': {'type': 'session', 'params': {}},  # single-line format
                'sessionIsMarket': {'type': 'session', 'params': {}},  # single-line format
                'sessionIsPostMarket': {'type': 'session', 'params': {}},  # single-line format
                'sessionIsPreMarket': {'type': 'session', 'params': {}},  # single-line format
                'sessionRegular': {'type': 'session_constant', 'params': {}},  # single-line format
                'sessionExtended': {'type': 'session_constant', 'params': {}},  # single-line format
                'timeFormat': {'type': 'time', 'params': {'time': {'type': 'integer', 'required': True}, 'format': {'type': 'string', 'required': True}}},  # single-line format
                'timestamp': {'type': 'time', 'params': {'year': {'type': 'integer', 'required': True}, 'month': {'type': 'integer', 'required': True}, 'day': {'type': 'integer', 'required': True}, 'hour': {'type': 'integer', 'default': 0}, 'minute': {'type': 'integer', 'default': 0}, 'second': {'type': 'integer', 'default': 0}}},  # single-line format

                'dayOfWeekFriday': {'type': 'time_constant', 'params': {}},  # single-line format
                'dayOfWeekMonday': {'type': 'time_constant', 'params': {}},  # single-line format
                'dayOfWeekSaturday': {'type': 'time_constant', 'params': {}},  # single-line format
                'dayOfWeekSunday': {'type': 'time_constant', 'params': {}},  # single-line format
                'dayOfWeekThursday': {'type': 'time_constant', 'params': {}},  # single-line format
                'dayOfWeekTuesday': {'type': 'time_constant', 'params': {}},  # single-line format
                'dayOfWeekWednesday': {'type': 'time_constant', 'params': {}},  # single-line format
                'barStateIsConfirmed': {'type': 'bar_state', 'params': {}},  # single-line format
                'barStateIsFirst': {'type': 'bar_state', 'params': {}},  # single-line format
                'barStateIsHistory': {'type': 'bar_state', 'params': {}},  # single-line format
                'barStateIsLast': {'type': 'bar_state', 'params': {}},  # single-line format
                'barStateIsLastConfirmedHistory': {'type': 'bar_state', 'params': {}},  # single-line format
                'barStateIsNew': {'type': 'bar_state', 'params': {}},  # single-line format
                'barStateIsRealtime': {'type': 'bar_state', 'params': {}},  # single-line format

                'timeFromUnix': {'type': 'time', 'params': {'unix': {'type': 'integer', 'required': True}}},  # single-line format
                'timeToUnix': {'type': 'time', 'params': {'time': {'type': 'integer', 'required': True}}},  # single-line format
                'timeToString': {'type': 'time', 'params': {'time': {'type': 'integer', 'required': True}, 'timezone': {'type': 'string', 'optional': True}}},  # single-line format
                'timeSeriesCompare': {'type': 'time', 'params': {'time1': {'type': 'integer', 'required': True}, 'time2': {'type': 'integer', 'required': True}}},  # single-line format
                'barTime': {'type': 'time', 'params': {}},  # single-line format
                'lastBarTime': {'type': 'time', 'params': {}},  # single-line format
                'firstBarTime': {'type': 'time', 'params': {}},  # single-line format
                'time_close': {'type': 'time', 'params': {}},  # single-line format

                # SECTION: ARRAY FUNCTIONS
                'arrAbs': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrAvg': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrBinarySearch': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrConcat': {'type': 'array', 'params': {'array1': {'type': 'array', 'required': True}, 'array2': {'type': 'array', 'required': True}}},  # single-line format
                'arrCopy': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrFirst': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrLast': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrMax': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrMin': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format

                'arrPush': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrPop': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrShift': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrUnshift': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrSort': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'order': {'type': 'string', 'default': 'ascending'}}},  # single-line format
                'arrReverse': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrSlice': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'start': {'type': 'integer', 'required': True}, 'end': {'type': 'integer', 'optional': True}}},  # single-line format
                'arrMap': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'function': {'type': 'function', 'required': True}}},  # single-line format
                'arrReduce': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'function': {'type': 'function', 'required': True}, 'initialValue': {'type': 'any', 'optional': True}}},  # single-line format

                'arrFilter': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'function': {'type': 'function', 'required': True}}},  # single-line format
                'arrIndexOf': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}, 'fromIndex': {'type': 'integer', 'default': 0}}},  # single-line format
                'arrLastIndexOf': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}, 'fromIndex': {'type': 'integer', 'optional': True}}},  # single-line format
                'arrIncludes': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrSome': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'function': {'type': 'function', 'required': True}}},  # single-line format
                'arrEvery': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'function': {'type': 'function', 'required': True}}},  # single-line format
                'arrJoin': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'separator': {'type': 'string', 'default': ','}}},  # single-line format
                'arrFill': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}, 'start': {'type': 'integer', 'default': 0}, 'end': {'type': 'integer', 'optional': True}}},  # single-line format
                'arrSize': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrClear': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrStdev': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrVariance': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrMode': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrMedian': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrSum': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrProduct': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrNew': {'type': 'array', 'params': {'size': {'type': 'integer', 'required': True}, 'value': {'type': 'any', 'optional': True}}},  # single-line format
                'arrNewBool': {'type': 'array', 'params': {'size': {'type': 'integer', 'required': True}}},  # single-line format
                'arrNewInt': {'type': 'array', 'params': {'size': {'type': 'integer', 'required': True}}},  # single-line format
                'arrNewFloat': {'type': 'array', 'params': {'size': {'type': 'integer', 'required': True}}},  # single-line format
                'arrNewString': {'type': 'array', 'params': {'size': {'type': 'integer', 'required': True}}},  # single-line format
                'arrCovariance': {'type': 'array', 'params': {'array1': {'type': 'array', 'required': True}, 'array2': {'type': 'array', 'required': True}}},  # single-line format
                'arrPercentile': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'percentage': {'type': 'float', 'required': True}}},  # single-line format
                'arrPercentRank': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'float', 'required': True}}},  # single-line format
                'arrStandardize': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrRange': {'type': 'array', 'params': {'start': {'type': 'integer', 'required': True}, 'end': {'type': 'integer', 'required': True}, 'step': {'type': 'integer', 'default': 1}}},  # single-line format
                'arrGet': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'index': {'type': 'integer', 'required': True}}},  # single-line format
                'arrSet': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'index': {'type': 'integer', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrInsert': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'index': {'type': 'integer', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrRemove': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'index': {'type': 'integer', 'required': True}}},  # single-line format
                'arrFrom': {'type': 'array', 'params': {'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrBinarySearchLeftmost': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrBinarySearchRightmost': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'arrSortIndices': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrPercentileLinearInterpolation': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'percentage': {'type': 'float', 'required': True}}},  # single-line format
                'arrPercentileNearestRank': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'percentage': {'type': 'float', 'required': True}}},  # single-line format

                # SECTION: BOX FUNCTIONS
                'boxNew': {'type': 'box', 'params': {'left': {'type': 'integer', 'required': True}, 'top': {'type': 'integer', 'required': True}, 'right': {'type': 'integer', 'required': True}, 'bottom': {'type': 'integer', 'required': True}}},  # single-line format
                'boxCopy': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}}},  # single-line format
                'boxDelete': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}}},  # single-line format
                'boxGetLeft': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}}},  # single-line format
                'boxGetTop': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}}},  # single-line format
                'boxGetRight': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}}},  # single-line format
                'boxGetBottom': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}}},  # single-line format
                'boxSetLeft': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'value': {'type': 'integer', 'required': True}}},  # single-line format
                'boxSetTop': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'value': {'type': 'integer', 'required': True}}},  # single-line format
                'boxSetRight': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'value': {'type': 'integer', 'required': True}}},  # single-line format
                'boxSetBottom': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'value': {'type': 'integer', 'required': True}}},  # single-line format
                'boxSetBgColor': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'color': {'type': 'color', 'required': True}}},  # single-line format
                'boxSetBorderColor': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'color': {'type': 'color', 'required': True}}},  # single-line format
                'boxSetBorderStyle': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'style': {'type': 'string', 'required': True}}},  # single-line format
                'boxSetBorderWidth': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'width': {'type': 'integer', 'required': True}}},  # single-line format
                'boxSetText': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'text': {'type': 'string', 'required': True}}},  # single-line format
                'boxSetTextColor': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'color': {'type': 'color', 'required': True}}},  # single-line format
                'boxSetTextSize': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'size': {'type': 'integer', 'required': True}}},  # single-line format
                'boxSetTextAlign': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'align': {'type': 'string', 'required': True}}},  # single-line format
                'boxSetTextVAlign': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'valign': {'type': 'string', 'required': True}}},  # single-line format
                'boxSetTextWrap': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'wrap': {'type': 'string', 'required': True}}},  # single-line format

                # SECTION: COLOR FUNCTIONS
                'color': {'type': 'color', 'params': {'red': {'type': 'integer', 'required': True}, 'green': {'type': 'integer', 'required': True}, 'blue': {'type': 'integer', 'required': True}, 'transp': {'type': 'integer', 'default': 0}}},  # single-line format
                'colorRed': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colorGreen': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colorBlue': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colorAlpha': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colorToString': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colorFromString': {'type': 'color', 'params': {'string': {'type': 'string', 'required': True}}},  # single-line format
                'colorBlend': {'type': 'color', 'params': {'color1': {'type': 'color', 'required': True}, 'color2': {'type': 'color', 'required': True}, 'weight': {'type': 'float', 'required': True}}},  # single-line format
                'colorRgb': {'type': 'color', 'params': {'red': {'type': 'integer', 'required': True}, 'green': {'type': 'integer', 'required': True}, 'blue': {'type': 'integer', 'required': True}}},  # single-line format
                'colAqua': {'type': 'color', 'params': {}, 'value': '#00FFFF'},  # single-line format
                'colBlack': {'type': 'color', 'params': {}, 'value': '#000000'},  # single-line format
                'colBlue': {'type': 'color', 'params': {}, 'value': '#0000FF'},  # single-line format
                'colFuchsia': {'type': 'color', 'params': {}, 'value': '#FF00FF'},  # single-line format
                'colGray': {'type': 'color', 'params': {}, 'value': '#808080'},  # single-line format
                'colGreen': {'type': 'color', 'params': {}, 'value': '#008000'},  # single-line format
                'colLime': {'type': 'color', 'params': {}, 'value': '#00FF00'},  # single-line format
                'colMaroon': {'type': 'color', 'params': {}, 'value': '#800000'},  # single-line format
                'colNavy': {'type': 'color', 'params': {}, 'value': '#000080'},  # single-line format
                'colOlive': {'type': 'color', 'params': {}, 'value': '#808000'},  # single-line format
                'colOrange': {'type': 'color', 'params': {}, 'value': '#FFA500'},  # single-line format
                'colPurple': {'type': 'color', 'params': {}, 'value': '#800080'},  # single-line format
                'colRed': {'type': 'color', 'params': {}, 'value': '#FF0000'},  # single-line format
                'colSilver': {'type': 'color', 'params': {}, 'value': '#C0C0C0'},  # single-line format
                'colTeal': {'type': 'color', 'params': {}, 'value': '#008080'},  # single-line format
                'colWhite': {'type': 'color', 'params': {}, 'value': '#FFFFFF'},  # single-line format
                'colYellow': {'type': 'color', 'params': {}, 'value': '#FFFF00'},  # single-line format
                'colFromGradient': {'type': 'color', 'params': {'color1': {'type': 'color', 'required': True}, 'color2': {'type': 'color', 'required': True}, 'percentage': {'type': 'float', 'required': True}}},  # single-line format
                'colB': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colG': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colR': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format
                'colT': {'type': 'color', 'params': {'color': {'type': 'color', 'required': True}}},  # single-line format

                # Currencies
                'currencyAUD': {'type': 'currency', 'category': 'fiat', 'value': 'AUD'},  # single-line format
                'currencyBTC': {'type': 'currency', 'category': 'crypto', 'value': 'BTC'},  # single-line format
                'currencyCAD': {'type': 'currency', 'category': 'fiat', 'value': 'CAD'},  # single-line format
                'currencyCHF': {'type': 'currency', 'category': 'fiat', 'value': 'CHF'},  # single-line format
                'currencyETH': {'type': 'currency', 'category': 'crypto', 'value': 'ETH'},  # single-line format
                'currencyEUR': {'type': 'currency', 'category': 'fiat', 'value': 'EUR'},  # single-line format
                'currencyGBP': {'type': 'currency', 'category': 'fiat', 'value': 'GBP'},  # single-line format
                'currencyJPY': {'type': 'currency', 'category': 'fiat', 'value': 'JPY'},  # single-line format
                'currencyUSD': {'type': 'currency', 'category': 'fiat', 'value': 'USD'},  # single-line format
                'currencyUSDT': {'type': 'currency', 'category': 'crypto', 'value': 'USDT'},  # single-line format

                # Display Settings
                'displayAll': {'type': 'display', 'category': 'visibility', 'value': 'all'},  # single-line format
                'displayDataWindow': {'type': 'display', 'category': 'visibility', 'value': 'data_window'},  # single-line format
                'displayNone': {'type': 'display', 'category': 'visibility', 'value': 'none'},  # single-line format
                'displayPane': {'type': 'display', 'category': 'visibility', 'value': 'pane'},  # single-line format
                'displayPriceScale': {'type': 'display', 'category': 'visibility', 'value': 'price_scale'},  # single-line format
                'displayStatusLine': {'type': 'display', 'category': 'visibility', 'value': 'status_line'},  # single-line format

                # SECTION: INPUT FUNCTIONS
                'input': {'type': 'input', 'params': {'defval': {'type': 'any', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputInt': {'type': 'input', 'params': {'defval': {'type': 'integer', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'minval': {'type': 'integer', 'optional': True}, 'maxval': {'type': 'integer', 'optional': True}, 'step': {'type': 'integer', 'default': 1}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputFloat': {'type': 'input', 'params': {'defval': {'type': 'float', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'minval': {'type': 'float', 'optional': True}, 'maxval': {'type': 'float', 'optional': True}, 'step': {'type': 'float', 'default': 0.1}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputBool': {'type': 'input', 'params': {'defval': {'type': 'bool', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputString': {'type': 'input', 'params': {'defval': {'type': 'string', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputSymbol': {'type': 'input', 'params': {'defval': {'type': 'string', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputSource': {'type': 'input', 'params': {'defval': {'type': 'source', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputTime': {'type': 'input', 'params': {'defval': {'type': 'time', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputSession': {'type': 'input', 'params': {'defval': {'type': 'string', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputColor': {'type': 'input', 'params': {'defval': {'type': 'color', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputPrice': {'type': 'input', 'params': {'defval': {'type': 'float', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputTimeframe': {'type': 'input', 'params': {'defval': {'type': 'string', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputTextArea': {'type': 'input', 'params': {'defval': {'type': 'string', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format
                'inputEnum': {'type': 'input', 'params': {'defval': {'type': 'string', 'required': True}, 'title': {'type': 'string', 'optional': True}, 'options': {'type': 'array', 'required': True}, 'tooltip': {'type': 'string', 'optional': True}}},  # single-line format

                # SECTION: LABEL FUNCTIONS
                'labelNew': {'type': 'label', 'params': {'x': {'type': 'integer', 'required': True}, 'y': {'type': 'float', 'required': True}, 'text': {'type': 'string', 'required': True}, 'xloc': {'type': 'string', 'default': 'bar_index'}, 'yloc': {'type': 'string', 'default': 'price'}, 'color': {'type': 'color', 'optional': True}, 'style': {'type': 'string', 'optional': True}, 'textcolor': {'type': 'color', 'optional': True}, 'size': {'type': 'string', 'default': 'normal'}}},  # single-line format
                'labelDelete': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGet': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelSet': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'text': {'type': 'string', 'required': True}}},  # single-line format
                'labelSetColor': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'color': {'type': 'color', 'required': True}}},  # single-line format
                'labelSetStyle': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'style': {'type': 'string', 'required': True}}},  # single-line format
                'labelSetX': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'x': {'type': 'integer', 'required': True}}},  # single-line format
                'labelSetY': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'y': {'type': 'float', 'required': True}}},  # single-line format
                'labelSetText': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'text': {'type': 'string', 'required': True}}},  # single-line format
                'labelSetTextColor': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'color': {'type': 'color', 'required': True}}},  # single-line format
                'labelSetSize': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'size': {'type': 'string', 'required': True}}},  # single-line format
                'labelSetXLoc': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'xloc': {'type': 'string', 'required': True}}},  # single-line format
                'labelSetYLoc': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'yloc': {'type': 'string', 'required': True}}},  # single-line format
                'labelGetX': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetY': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetText': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetStyle': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelSetTooltip': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'tooltip': {'type': 'string', 'required': True}}},  # single-line format
                'labelSetTextFont': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'font_family': {'type': 'string', 'required': True}}},  # single-line format
                'labelSetTextAlign': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'align': {'type': 'string', 'required': True}}},  # single-line format
                'labelCopy': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelDeleteAll': {'type': 'label', 'params': {}},  # single-line format
                'labelGetAll': {'type': 'label', 'params': {}},  # single-line format
                'labelSetPoint': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}, 'point': {'type': 'point', 'required': True}}},  # single-line format
                'labelGetPoint': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetColor': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetTextColor': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetSize': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetXLoc': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format
                'labelGetYLoc': {'type': 'label', 'params': {'id': {'type': 'label', 'required': True}}},  # single-line format

                # More Array Functions
                'arrClear': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}}},  # single-line format
                'arrConcat': {'type': 'array', 'params': {'array1': {'type': 'array', 'required': True}, 'array2': {'type': 'array', 'required': True}}},  # single-line format
                'arrCovariance': {'type': 'array', 'params': {'array1': {'type': 'array', 'required': True}, 'array2': {'type': 'array', 'required': True}}},  # single-line format
                'arrEvery': {'type': 'array', 'params': {'array': {'type': 'array', 'required': True}, 'predicate': {'type': 'function', 'required': True}}},  # single-line format

                # More Box Functions
                'boxSetExtend': {'type': 'box', 'params': {'box': {'type': 'box', 'required': True}, 'extend': {'type': 'string', 'required': True}}},  # single-line format
                'boxAll': {'type': 'box', 'params': {}},  # single-line format

                # More Input Functions
                'inputSource': {'type': 'input', 'params': {'defval': {'type': 'source', 'required': True}, 'title': {'type': 'string', 'optional': True}}},  # single-line format
                'inputSeries': {'type': 'input', 'params': {'defval': {'type': 'series', 'required': True}, 'title': {'type': 'string', 'optional': True}}},  # single-line format

                # SECTION: LINE FUNCTIONS
                'lineNew': {'type': 'line', 'params': {'x1': {'type': 'integer', 'required': True}, 'y1': {'type': 'float', 'required': True}, 'x2': {'type': 'integer', 'required': True}, 'y2': {'type': 'float', 'required': True}, 'extend': {'type': 'string', 'optional': True}, 'color': {'type': 'color', 'optional': True}, 'style': {'type': 'string', 'optional': True}, 'width': {'type': 'integer', 'optional': True}}},  # single-line format
                'lineCopy': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineDelete': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineGetPrice': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'x': {'type': 'integer', 'required': True}}},  # single-line format
                'lineGetX1': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineGetX2': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineGetY1': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineGetY2': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineSetColor': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'color': {'type': 'color', 'required': True}}},  # single-line format
                'lineSetExtend': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'extend': {'type': 'string', 'required': True}}},  # single-line format
                'lineSetStyle': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'style': {'type': 'string', 'required': True}}},  # single-line format
                'lineSetWidth': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'width': {'type': 'integer', 'required': True}}},  # single-line format
                'lineSetX1': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'x': {'type': 'integer', 'required': True}}},  # single-line format
                'lineSetX2': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'x': {'type': 'integer', 'required': True}}},  # single-line format
                'lineSetY1': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'y': {'type': 'float', 'required': True}}},  # single-line format
                'lineSetY2': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'y': {'type': 'float', 'required': True}}},  # single-line format
                'lineSetXY1': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'x': {'type': 'integer', 'required': True}, 'y': {'type': 'float', 'required': True}}},  # single-line format
                'lineSetXY2': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'x': {'type': 'integer', 'required': True}, 'y': {'type': 'float', 'required': True}}},  # single-line format
                'lineSetFirstPoint': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'point': {'type': 'point', 'required': True}}},  # single-line format
                'lineSetSecondPoint': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'point': {'type': 'point', 'required': True}}},  # single-line format
                'lineSetXLoc': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'xloc': {'type': 'string', 'required': True}}},  # single-line format
                'lineAll': {'type': 'line', 'params': {}},  # single-line format
                'lineFill': {'type': 'line', 'params': {'line1': {'type': 'line', 'required': True}, 'line2': {'type': 'line', 'required': True}, 'color': {'type': 'color', 'optional': True}}},  # single-line format
                'lineFillAll': {'type': 'line', 'params': {}},  # single-line format
                'lineFillDelete': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineFillGetLine1': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineFillGetLine2': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineFillNew': {'type': 'line', 'params': {'line1': {'type': 'line', 'required': True}, 'line2': {'type': 'line', 'required': True}, 'color': {'type': 'color', 'optional': True}}},  # single-line format
                'lineFillSetColor': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}, 'color': {'type': 'color', 'required': True}}},  # single-line format
                'lineDeleteAll': {'type': 'line', 'params': {}},  # single-line format
                'lineGetAll': {'type': 'line', 'params': {}},  # single-line format
                'lineGetStyle': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineGetWidth': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format
                'lineGetExtend': {'type': 'line', 'params': {'id': {'type': 'line', 'required': True}}},  # single-line format

                # SECTION: MATH FUNCTIONS
                'mathAbs': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathAcos': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathAsin': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathAtan': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathCeil': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathCos': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathExp': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathFloor': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathLog': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathLog10': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathMax': {'type': 'math', 'params': {'value1': {'type': 'float', 'required': True}, 'value2': {'type': 'float', 'required': True}}},  # single-line format
                'mathMin': {'type': 'math', 'params': {'value1': {'type': 'float', 'required': True}, 'value2': {'type': 'float', 'required': True}}},  # single-line format
                'mathPow': {'type': 'math', 'params': {'base': {'type': 'float', 'required': True}, 'exponent': {'type': 'float', 'required': True}}},  # single-line format
                'mathRound': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathSign': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathSin': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathSqrt': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathTan': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathRandom': {'type': 'math', 'params': {'min': {'type': 'float', 'optional': True}, 'max': {'type': 'float', 'optional': True}}},  # single-line format
                'mathRoundToMinTick': {'type': 'math', 'params': {'value': {'type': 'float', 'required': True}}},  # single-line format
                'mathSum': {'type': 'math', 'params': {'values': {'type': 'array', 'required': True}}},  # single-line format
                'mathToDegrees': {'type': 'math', 'params': {'radians': {'type': 'float', 'required': True}}},  # single-line format
                'mathToRadians': {'type': 'math', 'params': {'degrees': {'type': 'float', 'required': True}}},  # single-line format
                'mathAvg': {'type': 'math', 'params': {'values': {'type': 'array', 'required': True}}},  # single-line format
                'mathStdev': {'type': 'math', 'params': {'values': {'type': 'array', 'required': True}}},  # single-line format
                'mathVariance': {'type': 'math', 'params': {'values': {'type': 'array', 'required': True}}},  # single-line format
                'mathMode': {'type': 'math', 'params': {'values': {'type': 'array', 'required': True}}},  # single-line format
                'mathMedian': {'type': 'math', 'params': {'values': {'type': 'array', 'required': True}}},  # single-line format
                'mathE': {'type': 'math', 'params': {}},  # single-line format
                'mathPi': {'type': 'math', 'params': {}},  # single-line format
                'mathPhi': {'type': 'math', 'params': {}},  # single-line format
                'mathRPhi': {'type': 'math', 'params': {}},  # single-line format

                # SECTION: MATRIX FUNCTIONS
                'matrixNew': {'type': 'matrix', 'params': {'rows': {'type': 'integer', 'required': True}, 'cols': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixGet': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'row': {'type': 'integer', 'required': True}, 'col': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixSet': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'row': {'type': 'integer', 'required': True}, 'col': {'type': 'integer', 'required': True}, 'value': {'type': 'float', 'required': True}}},  # single-line format
                'matrixRows': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixCols': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixAdd': {'type': 'matrix', 'params': {'matrix1': {'type': 'matrix', 'required': True}, 'matrix2': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixSub': {'type': 'matrix', 'params': {'matrix1': {'type': 'matrix', 'required': True}, 'matrix2': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixMul': {'type': 'matrix', 'params': {'matrix1': {'type': 'matrix', 'required': True}, 'matrix2': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixTranspose': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixDet': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixInv': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixRank': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixTrace': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixEigenValues': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixEigenVectors': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixCopy': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixConcat': {'type': 'matrix', 'params': {'matrix1': {'type': 'matrix', 'required': True}, 'matrix2': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixRow': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'row': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixCol': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'col': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixDiff': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsSquare': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsDiagonal': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsSymmetric': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsIdentity': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsZero': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsTriangular': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixKron': {'type': 'matrix', 'params': {'matrix1': {'type': 'matrix', 'required': True}, 'matrix2': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixPinv': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixPow': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'power': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixReshape': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'rows': {'type': 'integer', 'required': True}, 'cols': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixAddRow': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'row': {'type': 'array', 'required': True}}},  # single-line format
                'matrixAddCol': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'col': {'type': 'array', 'required': True}}},  # single-line format
                'matrixRemoveRow': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'index': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixRemoveCol': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'index': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixSwapRows': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'row1': {'type': 'integer', 'required': True}, 'row2': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixSwapCols': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'col1': {'type': 'integer', 'required': True}, 'col2': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixSort': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixReverse': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixSum': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixAvg': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixMax': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixMin': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixMode': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixMedian': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixFill': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'value': {'type': 'float', 'required': True}}},  # single-line format
                'matrixSubMatrix': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}, 'startRow': {'type': 'integer', 'required': True}, 'endRow': {'type': 'integer', 'required': True}, 'startCol': {'type': 'integer', 'required': True}, 'endCol': {'type': 'integer', 'required': True}}},  # single-line format
                'matrixIsAntiDiagonal': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsAntiSymmetric': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsBinary': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format
                'matrixIsStochastic': {'type': 'matrix', 'params': {'matrix': {'type': 'matrix', 'required': True}}},  # single-line format

                # SECTION: TIME FUNCTIONS
                'time': {'type': 'time', 'params': {'timezone': {'type': 'string', 'optional': True}}},  # single-line format
                'timeNow': {'type': 'time', 'params': {}},  # single-line format
                'timeClose': {'type': 'time', 'params': {}},  # single-line format
                'timeTradingDay': {'type': 'time', 'params': {}},  # single-line format
                'year': {'type': 'time', 'params': {}},  # single-line format
                'month': {'type': 'time', 'params': {}},  # single-line format
                'weekOfYear': {'type': 'time', 'params': {}},  # single-line format
                'dayOfMonth': {'type': 'time', 'params': {}},  # single-line format
                'dayOfWeek': {'type': 'time', 'params': {}},  # single-line format
                'hour': {'type': 'time', 'params': {}},  # single-line format
                'minute': {'type': 'time', 'params': {}},  # single-line format
                'second': {'type': 'time', 'params': {}},  # single-line format

                # String Operations
                'strContains': {'type': 'string', 'category': 'search', 'operation': 'contains'},  # single-line format
                'strEndsWith': {'type': 'string', 'category': 'search', 'operation': 'ends_with'},  # single-line format
                'strFormat': {'type': 'string', 'category': 'formatting', 'operation': 'format'},  # single-line format
                'strLength': {'type': 'string', 'category': 'property', 'operation': 'length'},  # single-line format
                'strLower': {'type': 'string', 'category': 'case', 'operation': 'lowercase'},  # single-line format
                'strMatch': {'type': 'string', 'category': 'search', 'operation': 'match'},  # single-line format
                'strPos': {'type': 'string', 'category': 'search', 'operation': 'position'},  # single-line format
                'strReplace': {'type': 'string', 'category': 'modification', 'operation': 'replace'},  # single-line format
                'strReplaceAll': {'type': 'string', 'category': 'modification', 'operation': 'replace_all'},  # single-line format
                'strSplit': {'type': 'string', 'category': 'modification', 'operation': 'split'},  # single-line format
                'strStartsWith': {'type': 'string', 'category': 'search', 'operation': 'starts_with'},  # single-line format
                'strSubstring': {'type': 'string', 'category': 'modification', 'operation': 'substring'},  # single-line format
                'strToNumber': {'type': 'string', 'category': 'conversion', 'operation': 'to_number'},  # single-line format
                'strToString': {'type': 'string', 'category': 'conversion', 'operation': 'to_string'},  # single-line format
                'strTrim': {'type': 'string', 'category': 'modification', 'operation': 'trim'},  # single-line format
                'strUpper': {'type': 'string', 'category': 'case', 'operation': 'uppercase'},  # single-line format

                # Chart Functions
                'chartPointCopy': {'type': 'chart', 'category': 'point', 'operation': 'copy'},  # single-line format
                'chartPointFromIndex': {'type': 'chart', 'category': 'point', 'operation': 'from_index'},  # single-line format
                'chartPointFromTime': {'type': 'chart', 'category': 'point', 'operation': 'from_time'},  # single-line format
                'chartPointNew': {'type': 'chart', 'category': 'point', 'operation': 'new'},  # single-line format
                'chartPointNow': {'type': 'chart', 'category': 'point', 'operation': 'now'},  # single-line format

                # Timeframe Operations
                'timeframeIsDaily': {'type': 'timeframe', 'category': 'check', 'operation': 'is_daily'},  # single-line format
                'timeframeIsDWM': {'type': 'timeframe', 'category': 'check', 'operation': 'is_dwm'},  # single-line format
                'timeframeIsIntraday': {'type': 'timeframe', 'category': 'check', 'operation': 'is_intraday'},  # single-line format
                'timeframeIsMinutes': {'type': 'timeframe', 'category': 'check', 'operation': 'is_minutes'},  # single-line format
                'timeframeIsMonthly': {'type': 'timeframe', 'category': 'check', 'operation': 'is_monthly'},  # single-line format
                'timeframeIsSeconds': {'type': 'timeframe', 'category': 'check', 'operation': 'is_seconds'},  # single-line format
                'timeframeIsTicks': {'type': 'timeframe', 'category': 'check', 'operation': 'is_ticks'},  # single-line format
                'timeframeIsWeekly': {'type': 'timeframe', 'category': 'check', 'operation': 'is_weekly'},  # single-line format
                'timeframeMainPeriod': {'type': 'timeframe', 'category': 'property', 'operation': 'main_period'},  # single-line format
                'timeframeMultiplier': {'type': 'timeframe', 'category': 'property', 'operation': 'multiplier'},  # single-line format
                'timeframePeriod': {'type': 'timeframe', 'category': 'property', 'operation': 'period'},  # single-line format

                # Table Functions
                'tableNew': {'type': 'table', 'params': {'columns': {'type': 'integer', 'required': True}, 'rows': {'type': 'integer', 'required': True}}},  # single-line format
                'tableCell': {'type': 'table', 'params': {'table': {'type': 'table', 'required': True}, 'column': {'type': 'integer', 'required': True}, 'row': {'type': 'integer', 'required': True}}},  # single-line format
                'tableCellSet': {'type': 'table', 'params': {'table': {'type': 'table', 'required': True}, 'column': {'type': 'integer', 'required': True}, 'row': {'type': 'integer', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'tableDelete': {'type': 'table', 'params': {'table': {'type': 'table', 'required': True}}},  # single-line format
                'tableClear': {'type': 'table', 'params': {'table': {'type': 'table', 'required': True}}},  # single-line format
                'tableAll': {'type': 'table', 'params': {}},  # single-line format

                # Request Functions
                'requestSecurity': {'type': 'request', 'params': {'symbol': {'type': 'string', 'required': True}, 'resolution': {'type': 'string', 'required': True}, 'expression': {'type': 'string', 'required': True}}},  # single-line format
                'requestEconomic': {'type': 'request', 'params': {'country': {'type': 'string', 'required': True}, 'field': {'type': 'string', 'required': True}}},  # single-line format
                'requestFinancial': {'type': 'request', 'params': {'symbol': {'type': 'string', 'required': True}, 'field': {'type': 'string', 'required': True}}},  # single-line format
                'requestQuandl': {'type': 'request', 'params': {'code': {'type': 'string', 'required': True}, 'field': {'type': 'string', 'required': True}}},  # single-line format

                # Alert Functions
                'alert': {'type': 'alert', 'params': {'message': {'type': 'string', 'required': True}, 'freq': {'type': 'string', 'optional': True}}},  # single-line format
                'alertCondition': {'type': 'alert', 'params': {'condition': {'type': 'bool', 'required': True}, 'message': {'type': 'string', 'required': True}}},  # single-line format

                # Log Functions
                'logInfo': {'type': 'log', 'params': {'message': {'type': 'string', 'required': True}}},  # single-line format
                'logWarning': {'type': 'log', 'params': {'message': {'type': 'string', 'required': True}}},  # single-line format
                'logError': {'type': 'log', 'params': {'message': {'type': 'string', 'required': True}}},  # single-line format

                # Adjustment Constants
                'backAdjustmentInherit': {'type': 'adjustment', 'category': 'back', 'operation': 'inherit'},  # single-line format
                'backAdjustmentOff': {'type': 'adjustment', 'category': 'back', 'operation': 'off'},  # single-line format
                'backAdjustmentOn': {'type': 'adjustment', 'category': 'back', 'operation': 'on'},  # single-line format
                'settlementAsCloseInherit': {'type': 'adjustment', 'category': 'settlement', 'operation': 'inherit'},  # single-line format
                'settlementAsCloseOff': {'type': 'adjustment', 'category': 'settlement', 'operation': 'off'},  # single-line format
                'settlementAsCloseOn': {'type': 'adjustment', 'category': 'settlement', 'operation': 'on'},  # single-line format

                # Format Settings
                'formatInherit': {'type': 'format', 'category': 'inheritance', 'operation': 'inherit'},  # single-line format
                'formatMinTick': {'type': 'format', 'category': 'price', 'operation': 'min_tick'},  # single-line format
                'formatPercent': {'type': 'format', 'category': 'number', 'operation': 'percent'},  # single-line format
                'formatPrice': {'type': 'format', 'category': 'price', 'operation': 'price'},  # single-line format
                'formatVolume': {'type': 'format', 'category': 'volume', 'operation': 'volume'},  # single-line format

                # Earnings and Dividends
                'earningsActual': {'type': 'earnings', 'category': 'report', 'operation': 'actual'},  # single-line format
                'earningsEstimate': {'type': 'earnings', 'category': 'report', 'operation': 'estimate'},  # single-line format
                'earningsStandardized': {'type': 'earnings', 'category': 'report', 'operation': 'standardized'},  # single-line format
                'dividendsGross': {'type': 'dividends', 'category': 'payment', 'operation': 'gross'},  # single-line format
                'dividendsNet': {'type': 'dividends', 'category': 'payment', 'operation': 'net'},  # single-line format
                'dividendsFutureAmount': {'type': 'dividends', 'category': 'future', 'operation': 'amount'},  # single-line format
                'dividendsFutureExDate': {'type': 'dividends', 'category': 'future', 'operation': 'ex_date'},  # single-line format
                'dividendsFuturePayDate': {'type': 'dividends', 'category': 'future', 'operation': 'pay_date'},  # single-line format

                # Order Management
                'strategyOcaCancel': {'type': 'order', 'category': 'oca', 'operation': 'cancel'},  # single-line format
                'strategyOcaNone': {'type': 'order', 'category': 'oca', 'operation': 'none'},  # single-line format
                'strategyOcaReduce': {'type': 'order', 'category': 'oca', 'operation': 'reduce'},  # single-line format
                'strategyPercentOfEquity': {'type': 'order', 'category': 'sizing', 'operation': 'percent_of_equity'},  # single-line format

                # Session Types
                'sessionExtended': {'type': 'session', 'category': 'type', 'operation': 'extended'},  # single-line format
                'sessionRegular': {'type': 'session', 'category': 'type', 'operation': 'regular'},  # single-line format
                'sessionIsPreMarket': {'type': 'session', 'category': 'check', 'operation': 'is_pre_market'},  # single-line format
                'sessionIsPostMarket': {'type': 'session', 'category': 'check', 'operation': 'is_post_market'},  # single-line format
                'sessionIsMarket': {'type': 'session', 'category': 'check', 'operation': 'is_market'},  # single-line format

                # Chart Elements
                'boxAll': {'type': 'chart', 'category': 'collection', 'items': 'box'},  # single-line format
                'chartBgCol': {'type': 'chart', 'category': 'color', 'default': 'white'},  # single-line format
                'chartFgCol': {'type': 'chart', 'category': 'color', 'default': 'black'},  # single-line format
                'chartIsHeikinAshi': {'type': 'chart', 'category': 'type', 'default': False},  # single-line format
                'chartIsKagi': {'type': 'chart', 'category': 'type', 'default': False},  # single-line format
                'chartIsLineBreak': {'type': 'chart', 'category': 'type', 'default': False},  # single-line format
                'chartIsPnf': {'type': 'chart', 'category': 'type', 'default': False},  # single-line format
                'chartIsRange': {'type': 'chart', 'category': 'type', 'default': False},  # single-line format
                'chartIsRenko': {'type': 'chart', 'category': 'type', 'default': False},  # single-line format
                'chartIsStandard': {'type': 'chart', 'category': 'type', 'default': True},  # single-line format
                'chartLeftVisibleBarTime': {'type': 'chart', 'category': 'time', 'default': 0},  # single-line format
                'chartRightVisibleBarTime': {'type': 'chart', 'category': 'time', 'default': 0},  # single-line format
                'labelAll': {'type': 'chart', 'category': 'collection', 'items': 'label'},  # single-line format
                'lineAll': {'type': 'chart', 'category': 'collection', 'items': 'line'},  # single-line format
                'lineFillAll': {'type': 'chart', 'category': 'collection', 'items': 'lineFill'},  # single-line format
                'polylineAll': {'type': 'chart', 'category': 'collection', 'items': 'polyline'},  # single-line format
                'tableAll': {'type': 'chart', 'category': 'collection', 'items': 'table'},  # single-line format

                # Control Flow
                'andOp': {'type': 'control', 'category': 'logical', 'operation': 'and'},  # single-line format
                'enumType': {'type': 'control', 'category': 'type', 'operation': 'enum'},  # single-line format
                'exportFunc': {'type': 'control', 'category': 'module', 'operation': 'export'},  # single-line format
                'forLoop': {'type': 'control', 'category': 'loop', 'operation': 'for'},  # single-line format
                'forInLoop': {'type': 'control', 'category': 'loop', 'operation': 'forIn'},  # single-line format
                'ifCond': {'type': 'control', 'category': 'conditional', 'operation': 'if'},  # single-line format
                'importFunc': {'type': 'control', 'category': 'module', 'operation': 'import'},  # single-line format
                'methodFunc': {'type': 'control', 'category': 'function', 'operation': 'method'},  # single-line format
                'notOp': {'type': 'control', 'category': 'logical', 'operation': 'not'},  # single-line format
                'orOp': {'type': 'control', 'category': 'logical', 'operation': 'or'},  # single-line format
                'switchCase': {'type': 'control', 'category': 'conditional', 'operation': 'switch'},  # single-line format
                'typeDef': {'type': 'control', 'category': 'type', 'operation': 'typedef'},  # single-line format
                'whileLoop': {'type': 'control', 'category': 'loop', 'operation': 'while'},  # single-line format

                # Operators
                '=': {'type': 'operator', 'category': 'assignment'},  # single-line format
                '+': {'type': 'operator', 'category': 'arithmetic'},  # single-line format
                '-': {'type': 'operator', 'category': 'arithmetic'},  # single-line format
                '*': {'type': 'operator', 'category': 'arithmetic'},  # single-line format
                '/': {'type': 'operator', 'category': 'arithmetic'},  # single-line format
                '%': {'type': 'operator', 'category': 'arithmetic'},  # single-line format
                '==': {'type': 'operator', 'category': 'comparison'},  # single-line format
                '!=': {'type': 'operator', 'category': 'comparison'},  # single-line format
                '>': {'type': 'operator', 'category': 'comparison'},  # single-line format
                '<': {'type': 'operator', 'category': 'comparison'},  # single-line format
                '>=': {'type': 'operator', 'category': 'comparison'},  # single-line format
                '<=': {'type': 'operator', 'category': 'comparison'},  # single-line format

                # Day of Week Constants
                'dayOfWeekSunday': {'type': 'time', 'category': 'day', 'value': 0},  # single-line format
                'dayOfWeekMonday': {'type': 'time', 'category': 'day', 'value': 1},  # single-line format
                'dayOfWeekTuesday': {'type': 'time', 'category': 'day', 'value': 2},  # single-line format
                'dayOfWeekWednesday': {'type': 'time', 'category': 'day', 'value': 3},  # single-line format
                'dayOfWeekThursday': {'type': 'time', 'category': 'day', 'value': 4},  # single-line format
                'dayOfWeekFriday': {'type': 'time', 'category': 'day', 'value': 5},  # single-line format
                'dayOfWeekSaturday': {'type': 'time', 'category': 'day', 'value': 6},  # single-line format

                # Location Types
                'locationAboveBar': {'type': 'location', 'category': 'vertical', 'value': 'above_bar'},  # single-line format
                'locationAbsolute': {'type': 'location', 'category': 'positioning', 'value': 'absolute'},  # single-line format
                'locationBelowBar': {'type': 'location', 'category': 'vertical', 'value': 'below_bar'},  # single-line format
                'locationBottom': {'type': 'location', 'category': 'vertical', 'value': 'bottom'},  # single-line format
                'locationTop': {'type': 'location', 'category': 'vertical', 'value': 'top'},  # single-line format

                # Scale Types
                'scaleLeft': {'type': 'scale', 'category': 'position', 'value': 'left'},  # single-line format
                'scaleNone': {'type': 'scale', 'category': 'visibility', 'value': 'none'},  # single-line format
                'scaleRight': {'type': 'scale', 'category': 'position', 'value': 'right'},  # single-line format

                # Boolean Values
                'trueValue': {'type': 'boolean', 'category': 'constant', 'value': True},  # single-line format
                'falseValue': {'type': 'boolean', 'category': 'constant', 'value': False},  # single-line format

                # Map Functions
                'mapNew': {'type': 'map', 'params': {}},  # single-line format
                'mapGet': {'type': 'map', 'params': {'map': {'type': 'map', 'required': True}, 'key': {'type': 'string', 'required': True}}},  # single-line format
                'mapSet': {'type': 'map', 'params': {'map': {'type': 'map', 'required': True}, 'key': {'type': 'string', 'required': True}, 'value': {'type': 'any', 'required': True}}},  # single-line format
                'mapKeys': {'type': 'map', 'params': {'map': {'type': 'map', 'required': True}}},  # single-line format
                'mapValues': {'type': 'map', 'params': {'map': {'type': 'map', 'required': True}}},  # single-line format
                'mapSize': {'type': 'map', 'params': {'map': {'type': 'map', 'required': True}}},  # single-line format

                # Bar State Indicators
                'barIndex': {'type': 'bar', 'category': 'state', 'operation': 'index'},  # single-line format
                'barStateIsConfirmed': {'type': 'bar', 'category': 'state', 'operation': 'is_confirmed'},  # single-line format
                'barStateIsFirst': {'type': 'bar', 'category': 'state', 'operation': 'is_first'},  # single-line format
                'barStateIsHistory': {'type': 'bar', 'category': 'state', 'operation': 'is_history'},  # single-line format
                'barStateIsLast': {'type': 'bar', 'category': 'state', 'operation': 'is_last'},  # single-line format
                'barStateIsLastConfirmedHistory': {'type': 'bar', 'category': 'state', 'operation': 'is_last_confirmed_history'},  # single-line format
                'barStateIsNew': {'type': 'bar', 'category': 'state', 'operation': 'is_new'},  # single-line format
                'barStateIsRealtime': {'type': 'bar', 'category': 'state', 'operation': 'is_realtime'},  # single-line format

                # Text Alignment
                'textAlignBottom': {'type': 'text', 'category': 'alignment', 'value': 'bottom'},  # single-line format
                'textAlignCenter': {'type': 'text', 'category': 'alignment', 'value': 'center'},  # single-line format
                'textAlignLeft': {'type': 'text', 'category': 'alignment', 'value': 'left'},  # single-line format
                'textAlignRight': {'type': 'text', 'category': 'alignment', 'value': 'right'},  # single-line format
                'textAlignTop': {'type': 'text', 'category': 'alignment', 'value': 'top'},  # single-line format
                'textWrapAuto': {'type': 'text', 'category': 'wrap', 'value': 'auto'},  # single-line format
                'textWrapNone': {'type': 'text', 'category': 'wrap', 'value': 'none'},  # single-line format

                # Location Types
                'xLocBarIndex': {'type': 'location', 'category': 'x_axis', 'value': 'bar_index'},  # single-line format
                'xLocBarTime': {'type': 'location', 'category': 'x_axis', 'value': 'bar_time'},  # single-line format
                'yLocAboveBar': {'type': 'location', 'category': 'y_axis', 'value': 'above_bar'},  # single-line format
                'yLocBelowBar': {'type': 'location', 'category': 'y_axis', 'value': 'below_bar'},  # single-line format
                'yLocPrice': {'type': 'location', 'category': 'y_axis', 'value': 'price'},  # single-line format

                # Shapes
                'shapeArrowDown': {'type': 'shape', 'category': 'arrow', 'value': 'arrow_down'},  # single-line format
                'shapeArrowUp': {'type': 'shape', 'category': 'arrow', 'value': 'arrow_up'},  # single-line format
                'shapeCircle': {'type': 'shape', 'category': 'basic', 'value': 'circle'},  # single-line format
                'shapeCross': {'type': 'shape', 'category': 'basic', 'value': 'cross'},  # single-line format
                'shapeDiamond': {'type': 'shape', 'category': 'basic', 'value': 'diamond'},  # single-line format
                'shapeFlag': {'type': 'shape', 'category': 'basic', 'value': 'flag'},  # single-line format
                'shapeLabelDown': {'type': 'shape', 'category': 'label', 'value': 'label_down'},  # single-line format
                'shapeLabelUp': {'type': 'shape', 'category': 'label', 'value': 'label_up'},  # single-line format
                'shapeSquare': {'type': 'shape', 'category': 'basic', 'value': 'square'},  # single-line format
                'shapeTriangleDown': {'type': 'shape', 'category': 'basic', 'value': 'triangle_down'},  # single-line format
                'shapeTriangleUp': {'type': 'shape', 'category': 'basic', 'value': 'triangle_up'},  # single-line format
                'shapeXCross': {'type': 'shape', 'category': 'basic', 'value': 'xcross'},  # single-line format

                # Sizes
                'sizeAuto': {'type': 'size', 'category': 'auto', 'value': 'auto'},  # single-line format
                'sizeHuge': {'type': 'size', 'category': 'fixed', 'value': 'huge'},  # single-line format
                'sizeLarge': {'type': 'size', 'category': 'fixed', 'value': 'large'},  # single-line format
                'sizeNormal': {'type': 'size', 'category': 'fixed', 'value': 'normal'},  # single-line format
                'sizeSmall': {'type': 'size', 'category': 'fixed', 'value': 'small'},  # single-line format
                'sizeTiny': {'type': 'size', 'category': 'fixed', 'value': 'tiny'},  # single-line format

                # Data Types
                'Numeric': {'type': 'datatype', 'category': 'primitive', 'value': 'numeric'},  # single-line format
                'Boolean': {'type': 'datatype', 'category': 'primitive', 'value': 'boolean'},  # single-line format
                'String': {'type': 'datatype', 'category': 'primitive', 'value': 'string'},  # single-line format
                'Series': {'type': 'datatype', 'category': 'complex', 'value': 'series'},  # single-line format

                'symInfoBaseCurrency': {'type': 'string', 'value': None, 'description': 'Base currency of the symbol'},  # single-line format
                'symInfoCountry': {'type': 'string', 'value': None, 'description': 'Country of the symbol'},  # single-line format
                'symInfoCurrency': {'type': 'string', 'value': None, 'description': 'Currency of the symbol'},  # single-line format
                'symInfoDescription': {'type': 'string', 'value': None, 'description': 'Description of the symbol'},  # single-line format
                'symInfoEmployees': {'type': 'integer', 'value': None, 'description': 'Number of employees'},  # single-line format
                'symInfoExpirationDate': {'type': 'time', 'value': None, 'description': 'Expiration date of the symbol'},  # single-line format
                'symInfoIndustry': {'type': 'string', 'value': None, 'description': 'Industry of the symbol'},  # single-line format
                'symInfoMainTickerId': {'type': 'string', 'value': None, 'description': 'Main ticker ID'},  # single-line format
                'symInfoMinContract': {'type': 'float', 'value': None, 'description': 'Minimum contract size'},  # single-line format
                'symInfoRecommendationsBuy': {'type': 'integer', 'value': None, 'description': 'Number of buy recommendations'},  # single-line format
                'symInfoRecommendationsBuyStrong': {'type': 'integer', 'value': None, 'description': 'Number of strong buy recommendations'},  # single-line format
                'symInfoRecommendationsDate': {'type': 'time', 'value': None, 'description': 'Date of recommendations'},  # single-line format
                'symInfoRecommendationsHold': {'type': 'integer', 'value': None, 'description': 'Number of hold recommendations'},  # single-line format
                'symInfoRecommendationsSell': {'type': 'integer', 'value': None, 'description': 'Number of sell recommendations'},  # single-line format
                'symInfoRecommendationsSellStrong': {'type': 'integer', 'value': None, 'description': 'Number of strong sell recommendations'},  # single-line format
                'symInfoRecommendationsTotal': {'type': 'integer', 'value': None, 'description': 'Total number of recommendations'},  # single-line format
                'symInfoTargetPriceAverage': {'type': 'float', 'value': None, 'description': 'Average target price'},  # single-line format
                'symInfoTargetPriceDate': {'type': 'time', 'value': None, 'description': 'Date of target price'},  # single-line format
                'symInfoTargetPriceEstimates': {'type': 'integer', 'value': None, 'description': 'Number of price estimates'},  # single-line format
                'symInfoTargetPriceHigh': {'type': 'float', 'value': None, 'description': 'Highest target price'},  # single-line format
                'symInfoTargetPriceLow': {'type': 'float', 'value': None, 'description': 'Lowest target price'},  # single-line format
                'symInfoTargetPriceMedian': {'type': 'float', 'value': None, 'description': 'Median target price'},  # single-line format
                'symInfoVolumeType': {'type': 'string', 'value': None, 'description': 'Type of volume data'},  # single-line format

                'requestCurrencyRate': {'type': 'function', 'params': {'from_currency': {'type': 'string'}, 'to_currency': {'type': 'string'}, 'timestamp': {'type': 'time'}}, 'returns': 'float'},  # single-line format
                'requestDividends': {'type': 'function', 'params': {'symbol': {'type': 'string'}, 'from_date': {'type': 'time'}, 'to_date': {'type': 'time'}}, 'returns': 'array'},  # single-line format
                'requestEarnings': {'type': 'function', 'params': {'symbol': {'type': 'string'}, 'from_date': {'type': 'time'}, 'to_date': {'type': 'time'}}, 'returns': 'array'},  # single-line format
                'requestEconomic': {'type': 'function', 'params': {'indicator': {'type': 'string'}, 'from_date': {'type': 'time'}, 'to_date': {'type': 'time'}}, 'returns': 'array'},  # single-line format
                'requestFinancial': {'type': 'function', 'params': {'symbol': {'type': 'string'}, 'statement': {'type': 'string'}, 'period': {'type': 'string'}}, 'returns': 'array'},  # single-line format
                'requestQuandl': {'type': 'function', 'params': {'code': {'type': 'string'}, 'from_date': {'type': 'time'}, 'to_date': {'type': 'time'}}, 'returns': 'array'},  # single-line format
                'requestSecurity': {'type': 'function', 'params': {'symbol': {'type': 'string'}, 'resolution': {'type': 'string'}, 'from_date': {'type': 'time'}, 'to_date': {'type': 'time'}}, 'returns': 'array'},  # single-line format
                'requestSecurityLowerTf': {'type': 'function', 'params': {'symbol': {'type': 'string'}, 'resolution': {'type': 'string'}, 'from_date': {'type': 'time'}, 'to_date': {'type': 'time'}, 'timeframe': {'type': 'string'}}, 'returns': 'array'},  # single-line format
                'requestSeed': {'type': 'function', 'params': {'seed_value': {'type': 'integer'}}, 'returns': 'integer'},  # single-line format
                'requestSplits': {'type': 'function', 'params': {'symbol': {'type': 'string'}, 'from_date': {'type': 'time'}, 'to_date': {'type': 'time'}}, 'returns': 'array'},  # single-line format

                'runtimeError': {'type': 'function', 'params': {'message': {'type': 'string'}}, 'returns': 'void'},  # single-line format
                'fixNan': {'type': 'function', 'params': {'value': {'type': 'float'}, 'replacement': {'type': 'float'}}, 'returns': 'float'},  # single-line format
                'nz': {'type': 'function', 'params': {'value': {'type': 'series'}, 'replacement': {'type': 'series', 'optional': True}}, 'returns': 'series'},  # single-line format
                'na': {'type': 'function', 'params': {'value': {'type': 'series'}}, 'returns': 'bool'},  # single-line format

                'barCol': {'type': 'function', 'params': {'color': {'type': 'color'}}, 'returns': 'void'},  # single-line format
                'maxBarsBack': {'type': 'function', 'params': {'buffer': {'type': 'series'}, 'max_bars': {'type': 'integer'}}, 'returns': 'void'},  # single-line format
                'library': {'type': 'function', 'params': {'name': {'type': 'string'}, 'version': {'type': 'string'}, 'code': {'type': 'string'}}, 'returns': 'void'},  # single-line format

                'barMergeGapsOff': {'type': 'const', 'value': 'barmerge_gaps_off', 'returns': 'string'},  # single-line format
                'barMergeGapsOn': {'type': 'const', 'value': 'barmerge_gaps_on', 'returns': 'string'},  # single-line format
                'barMergeLookaheadOff': {'type': 'const', 'value': 'barmerge_lookahead_off', 'returns': 'string'},  # single-line format
                'barMergeLookaheadOn': {'type': 'const', 'value': 'barmerge_lookahead_on', 'returns': 'string'},  # single-line format

                'currencyHKD': {'type': 'const', 'value': 'HKD', 'returns': 'string'},  # single-line format
                'currencyINR': {'type': 'const', 'value': 'INR', 'returns': 'string'},  # single-line format
                'currencyKRW': {'type': 'const', 'value': 'KRW', 'returns': 'string'},  # single-line format
                'currencyMYR': {'type': 'const', 'value': 'MYR', 'returns': 'string'},  # single-line format
                'currencyNOK': {'type': 'const', 'value': 'NOK', 'returns': 'string'},  # single-line format
                'currencyNone': {'type': 'const', 'value': 'NONE', 'returns': 'string'},  # single-line format
                'currencyNZD': {'type': 'const', 'value': 'NZD', 'returns': 'string'},  # single-line format
                'currencyRUB': {'type': 'const', 'value': 'RUB', 'returns': 'string'},  # single-line format
                'currencySEK': {'type': 'const', 'value': 'SEK', 'returns': 'string'},  # single-line format
                'currencySGD': {'type': 'const', 'value': 'SGD', 'returns': 'string'},  # single-line format
                'currencyTRY': {'type': 'const', 'value': 'TRY', 'returns': 'string'},  # single-line format
                'currencyZAR': {'type': 'const', 'value': 'ZAR', 'returns': 'string'},  # single-line format

                'labelStyleLabelCenter': {'type': 'const', 'value': 'label_style_label_center', 'returns': 'string'},  # single-line format
                'labelStyleLabelLeft': {'type': 'const', 'value': 'label_style_label_left', 'returns': 'string'},  # single-line format
                'labelStyleLabelLowerLeft': {'type': 'const', 'value': 'label_style_label_lower_left', 'returns': 'string'},  # single-line format
                'labelStyleLabelLowerRight': {'type': 'const', 'value': 'label_style_label_lower_right', 'returns': 'string'},  # single-line format
                'labelStyleLabelRight': {'type': 'const', 'value': 'label_style_label_right', 'returns': 'string'},  # single-line format
                'labelStyleLabelUpperLeft': {'type': 'const', 'value': 'label_style_label_upper_left', 'returns': 'string'},  # single-line format
                'labelStyleLabelUpperRight': {'type': 'const', 'value': 'label_style_label_upper_right', 'returns': 'string'},  # single-line format
           
                # ta-lib new syntaxes
                'adLine': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'volume': {'type': 'series', 'required': True}}},
                'adOsc': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'volume': {'type': 'series', 'required': True}, 'fastperiod': {'type': 'integer', 'default': 3}, 'slowperiod': {'type': 'integer', 'default': 10}}},
                'adx': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'adxr': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'apo': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'fastperiod': {'type': 'integer', 'default': 12}, 'slowperiod': {'type': 'integer', 'default': 26}}},
                'aroon': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'aroonOsc': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'atr': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'avgPrice': {'type': 'indicator', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'bbands': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 20}, 'deviations': {'type': 'float', 'default': 2.0}}},
                'beta': {'type': 'indicator', 'params': {'series1': {'type': 'series', 'required': True}, 'series2': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 5}}},
                'bop': {'type': 'indicator', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'cci': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'cmo': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'correl': {'type': 'indicator', 'params': {'series1': {'type': 'series', 'required': True}, 'series2': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'dema': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'dx': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'ema': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'htDcPeriod': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}}},
                'htDcPhase': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}}},
                'htPhasor': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}}},
                'htSine': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}}},
                'htTrendline': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}}},
                'htTrendMode': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}}},
                'kama': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'linearReg': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'linearRegAngle': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'linearRegIntercept': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'linearRegSlope': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'ma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}, 'matype': {'type': 'integer', 'default': 0}}},
                'macd': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'fastperiod': {'type': 'integer', 'default': 12}, 'slowperiod': {'type': 'integer', 'default': 26}, 'signalperiod': {'type': 'integer', 'default': 9}}},
                'macdExt': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'fastperiod': {'type': 'integer', 'default': 12}, 'fastmatype': {'type': 'integer', 'default': 0}, 'slowperiod': {'type': 'integer', 'default': 26}, 'slowmatype': {'type': 'integer', 'default': 0}, 'signalperiod': {'type': 'integer', 'default': 9}, 'signalmatype': {'type': 'integer', 'default': 0}}},
                'macdFix': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'signalperiod': {'type': 'integer', 'default': 9}}},
                'mama': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'fastlimit': {'type': 'float', 'default': 0.5}, 'slowlimit': {'type': 'float', 'default': 0.05}}},
                'maxIndex': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'medPrice': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}}},
                'mfi': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'volume': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'midPoint': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'midPrice': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'minIndex': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'minMax': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'minMaxIndex': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'minusDI': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'minusDM': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'mom': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 10}}},
                'natr': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'obv': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'volume': {'type': 'series', 'required': True}}},
                'plusDI': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'plusDM': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'ppo': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'fastperiod': {'type': 'integer', 'default': 12}, 'slowperiod': {'type': 'integer', 'default': 26}, 'matype': {'type': 'integer', 'default': 0}}},
                'roc': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 10}}},
                'rocp': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 10}}},
                'rocr': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 10}}},
                'rocr100': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 10}}},
                'rsi': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'sar': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'acceleration': {'type': 'float', 'default': 0.02}, 'maximum': {'type': 'float', 'default': 0.2}}},
                'sarExt': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'startvalue': {'type': 'float', 'default': 0}, 'offsetonreverse': {'type': 'float', 'default': 0}, 'accelerationinitlong': {'type': 'float', 'default': 0.02}, 'accelerationlong': {'type': 'float', 'default': 0.02}, 'accelerationmaxlong': {'type': 'float', 'default': 0.2}, 'accelerationinitshort': {'type': 'float', 'default': 0.02}, 'accelerationshort': {'type': 'float', 'default': 0.02}, 'accelerationmaxshort': {'type': 'float', 'default': 0.2}}},
                'sma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'stdDev': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 5}, 'nbdev': {'type': 'float', 'default': 1.0}}},
                'stoch': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'fastk_period': {'type': 'integer', 'default': 5}, 'slowk_period': {'type': 'integer', 'default': 3}, 'slowk_matype': {'type': 'integer', 'default': 0}, 'slowd_period': {'type': 'integer', 'default': 3}, 'slowd_matype': {'type': 'integer', 'default': 0}}},
                'stochF': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'fastk_period': {'type': 'integer', 'default': 5}, 'fastd_period': {'type': 'integer', 'default': 3}, 'fastd_matype': {'type': 'integer', 'default': 0}}},
                'stochRsi': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}, 'fastk_period': {'type': 'integer', 'default': 5}, 'fastd_period': {'type': 'integer', 'default': 3}, 'fastd_matype': {'type': 'integer', 'default': 0}}},
                'sum': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                't3': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 5}, 'vfactor': {'type': 'float', 'default': 0.7}}},
                'tema': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'tRange': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'trima': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'trix': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},
                'tsf': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'typPrice': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'ultOsc': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period1': {'type': 'integer', 'default': 7}, 'period2': {'type': 'integer', 'default': 14}, 'period3': {'type': 'integer', 'default': 28}}},
                'variance': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 5}, 'nbdev': {'type': 'float', 'default': 1.0}}},
                'wclPrice': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'willr': {'type': 'indicator', 'params': {'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 14}}},
                'wma': {'type': 'indicator', 'params': {'source': {'type': 'series', 'required': True}, 'period': {'type': 'integer', 'default': 30}}},


                #pattern recognition
                'pattern2Crows': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'pattern3BlackCrows': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'pattern3Inside': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'pattern3LineStrike': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'pattern3StarsInSouth': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'pattern3WhiteSoldiers': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternAbandonedBaby': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'penetration': {'type': 'float', 'default': 0.3}}},
                'patternAdvanceBlock': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternBeltHold': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternBreakaway': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternClosingMarubozu': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternConcealBabySwallow': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternCounterattack': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternDarkCloud': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'penetration': {'type': 'float', 'default': 0.5}}},
                'patternDoji': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternDojiStar': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternDragonflyDoji': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternEngulfing': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternEveningDojiStar': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'penetration': {'type': 'float', 'default': 0.3}}},
                'patternEveningStar': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'penetration': {'type': 'float', 'default': 0.3}}},
                'patternGapSideSide': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternGravestoneDoji': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHammer': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHangingMan': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHarami': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHaramiCross': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHighWave': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHikkake': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHikkakeMod': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternHomingPigeon': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternIdentical3Crows': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternInNeck': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternInvertedHammer': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternKicking': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternKickingByLength': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternLadderBottom': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternLongLeggedDoji': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternLongLine': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternMarubozu': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternMatchingLow': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternMatHold': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'penetration': {'type': 'float', 'default': 0.5}}},
                'patternMorningDojiStar': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'penetration': {'type': 'float', 'default': 0.3}}},
                'patternMorningStar': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}, 'penetration': {'type': 'float', 'default': 0.3}}},
                'patternOnNeck': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternPiercing': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternRickshawMan': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternRiseFall3Methods': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternSeparatingLines': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternShootingStar': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternShortLine': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternSpinningTop': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternStalledPattern': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternStickSandwich': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternTakuri': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternTasukiGap': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternThrusting': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternTristar': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternUnique3River': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternUpsideGap2Crows': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}},
                'patternXsideGap3Methods': {'type': 'pattern', 'params': {'open': {'type': 'series', 'required': True}, 'high': {'type': 'series', 'required': True}, 'low': {'type': 'series', 'required': True}, 'close': {'type': 'series', 'required': True}}}


           
           
            }
        }
    }




"""==================================================================================================================="""

class Environment:
    def __init__(self):
        self.variables = {}
        self.series_data = {}
        self.current_bar = None
        self.max_bars_back = 5000
        self.syntax_list = self._get_syntax_list()  # Add this line
        self.registry = self._initialize_registries()
        self.bar_index = 0
        self.is_realtime = False
        self.is_confirmed = False
        self.time_series = []

    def _get_syntax_list(self):
        return {
            'open': True, 'high': True, 'low': True, 'close': True, 'volume': True,
            'barIndex': True, 'barStateIsConfirmed': True, 'barStateIsFirst': True,
            'barStateIsHistory': True, 'barStateIsLast': True, 'barStateIsLastConfirmedHistory': True,
            'barStateIsNew': True, 'barStateIsRealtime': True, 'boxAll': True,
            'chartBgCol': True, 'chartFgCol': True, 'chartIsHeikinAshi': True,
            'chartIsKagi': True, 'chartIsLineBreak': True, 'chartIsPnf': True,
            'chartIsRange': True, 'chartIsRenko': True, 'chartIsStandard': True,
            'chartLeftVisibleBarTime': True, 'chartRightVisibleBarTime': True,
            'dayOfMonth': True, 'dayOfWeek': True, 'dividendsFutureAmount': True,
            'dividendsFutureExDate': True, 'dividendsFuturePayDate': True,
            'earningsFutureEps': True, 'earningsFuturePeriodEndTime': True,
            'earningsFutureRevenue': True, 'earningsFutureTime': True,
            'hl2': True, 'hlc3': True, 'hlcc4': True, 'hour': True,
            'labelAll': True, 'lastBarIndex': True, 'lastBarTime': True,
            'lineAll': True, 'lineFillAll': True, 'minute': True, 'month': True,
            'na': True, 'ohlc4': True, 'polylineAll': True, 'second': True,
            'sessionIsFirstBar': True, 'sessionIsFirstBarRegular': True,
            'sessionIsLastBar': True, 'sessionIsLastBarRegular': True,
            'sessionIsMarket': True, 'sessionIsPostMarket': True,
            'sessionIsPreMarket': True, 'strategyAccountCurrency': True,
            'strategyAvgLosingTrade': True, 'strategyAvgLosingTradePercent': True,
            'strategyAvgTrade': True, 'strategyAvgTradePercent': True,
            'strategyAvgWinningTrade': True, 'strategyAvgWinningTradePercent': True,
            'strategyClosedTrades': True, 'strategyClosedTradesFirstIndex': True,
            'strategyEquity': True, 'strategyEvenTrades': True,
            'strategyGrossLoss': True, 'strategyGrossLossPercent': True,
            'strategyGrossProfit': True, 'strategyGrossProfitPercent': True,
            'strategyInitialCapital': True, 'strategyLossTrades': True,
            'strategyMarginLiquidationPrice': True, 'strategyMaxContractsHeldAll': True,
            'strategyMaxContractsHeldLong': True, 'strategyMaxContractsHeldShort': True,
            'strategyMaxDrawdown': True, 'strategyMaxDrawdownPercent': True,
            'strategyMaxRunup': True, 'strategyMaxRunupPercent': True,
            'strategyNetProfit': True, 'strategyNetProfitPercent': True,
            'strategyOpenProfit': True, 'strategyOpenProfitPercent': True,
            'strategyOpenTrades': True, 'strategyOpenTradesCapitalHeld': True,
            'strategyPositionAvgPrice': True, 'strategyPositionEntryName': True,
            'strategyPositionSize': True, 'strategyWinTrades': True,
            'symInfoBaseCurrency': True, 'symInfoCountry': True,
            'symInfoCurrency': True, 'symInfoDescription': True,
            'symInfoEmployees': True, 'symInfoExpirationDate': True,
            'symInfoIndustry': True, 'symInfoMainTickerId': True,
            'symInfoMinContract': True, 'symInfoMinMove': True,
            'symInfoMinTick': True, 'symInfoPointValue': True,
            'symInfoPrefix': True, 'symInfoPriceScale': True,
            'symInfoRoot': True, 'symInfoSector': True,
            'symInfoSession': True, 'symInfoShareholders': True,
            'symInfoSharesOutstandingFloat': True, 'symInfoSharesOutstandingTotal': True,
            'symInfoTargetPriceAverage': True, 'symInfoTargetPriceDate': True,
            'symInfoTargetPriceEstimates': True, 'symInfoTargetPriceHigh': True,
            'symInfoTargetPriceLow': True, 'symInfoTargetPriceMedian': True,
            'symInfoTicker': True, 'symInfoTickerId': True,
            'symInfoTimezone': True, 'symInfoType': True,
            'symInfoVolumeType': True, 'tableAll': True,
            'time': True, 'timeClose': True, 'timeTradingDay': True,
            'timeframeIsDaily': True, 'timeframeIsDWM': True,
            'timeframeIsIntraday': True, 'timeframeIsMinutes': True,
            'timeframeIsMonthly': True, 'timeframeIsSeconds': True,
            'timeframeIsTicks': True, 'timeframeIsWeekly': True,
            'timeframeMainPeriod': True, 'timeframeMultiplier': True,
            'timeframePeriod': True, 'timeNow': True,
            'weekOfYear': True, 'year': True,
    
    
                    # Technical Analysis Functions
            'sma': True, 'ema': True, 'rsi': True, 'minvalue': True, 'maxvalue': True,
            'taAccDist': True, 'taIII': True, 'taNVI': True, 'taOBV': True, 'taPVI': True,
            'taPVT': True, 'taTR': True, 'taVWAP': True, 'taWAD': True, 'taWVAD': True,
            'taAlma': True, 'taAtr': True, 'taBarsSince': True, 'taBb': True, 'taBbw': True,
            'taCci': True, 'taChange': True, 'taCmo': True, 'taCog': True, 'taCorrelation': True,
            'taCross': True, 'taCrossover': True, 'taCrossunder': True, 'taCum': True,
            'taDev': True, 'taDmi': True, 'taEma': True, 'taFalling': True, 'taHighest': True,
            'taHighestBars': True, 'taHma': True, 'taKc': True, 'taKcw': True, 'taLinReg': True,
            'taLowest': True, 'taLowestBars': True, 'taMacd': True, 'taMax': True, 'taMedian': True,
            'taMfi': True, 'taMin': True, 'taMode': True, 'taMom': True, 'taPercentile': True,
            'taPercentRank': True, 'taPivotHigh': True, 'taPivotLow': True, 'taRange': True,
            'taRising': True, 'taRma': True, 'taRoc': True, 'taRsi': True, 'taSar': True,
            'taSma': True, 'taStdev': True, 'taStoch': True, 'taSuperTrend': True, 'taSwma': True,
            'taTsi': True, 'taValueWhen': True, 'taVariance': True, 'taVwap': True, 'taVwma': True,
            'taWma': True, 'taWpr': True,
    
            # Array Functions
            'arrAbs': True, 'arrAvg': True, 'arrBinarySearch': True, 'arrBinarySearchLeftmost': True,
            'arrBinarySearchRightmost': True, 'arrClear': True, 'arrConcat': True, 'arrCopy': True,
            'arrCovariance': True, 'arrEvery': True, 'arrFill': True, 'arrFirst': True,
            'arrFrom': True, 'arrGet': True, 'arrIncludes': True, 'arrIndexOf': True,
            'arrInsert': True, 'arrJoin': True, 'arrLast': True, 'arrLastIndexOf': True,
            'arrMax': True, 'arrMedian': True, 'arrMin': True, 'arrMode': True,
            'arrNewBool': True, 'arrNewBox': True, 'aryNewCol': True, 'arrNewFloat': True,
            'arrNewInt': True, 'arrNewLabel': True, 'arrNewLine': True, 'arrNewLineFill': True,
            'arrNewString': True, 'arrNewTable': True, 'arrNewType': True,
            'arrPercentileLinearInterpolation': True, 'arrPercentileNearestRank': True,
            'arrPercentRank': True, 'arrPop': True, 'arrPush': True, 'arrRange': True,
            'arrRemove': True, 'arrReverse': True, 'arrSet': True, 'arrShift': True,
            'arrSize': True, 'arrSlice': True, 'arrSome': True, 'arrSort': True,
            'arrSortIndices': True, 'arrStandardize': True, 'arrStdev': True,
            'arrSum': True, 'arrUnshift': True, 'arrVariance': True,
    
            # Box Functions
            'boxFunc': True, 'boxCopyFunc': True, 'boxDeleteFunc': True,
            'boxGetBottomFunc': True, 'boxGetLeftFunc': True, 'boxGetRightFunc': True,
            'boxGetTopFunc': True, 'boxNewFunc': True, 'boxSetBgColFunc': True,
            'boxSetBorderColFunc': True, 'boxSetBorderStyleFunc': True,
            'boxSetBorderWidthFunc': True, 'boxSetBottomFunc': True,
            'boxSetBottomRightPointFunc': True, 'boxSetExtendFunc': True,
            'boxSetLeftFunc': True, 'boxSetLeftTopFunc': True, 'boxSetRightFunc': True,
            'boxSetRightBottomFunc': True, 'boxSetTextFunc': True, 'boxSetTextColFunc': True,
            'boxSetTextFontFamilyFunc': True, 'boxSetTextHAlignFunc': True,
            'boxSetTextSizeFunc': True, 'boxSetTextVAlignFunc': True,
            'boxSetTextWrapFunc': True, 'boxSetTopFunc': True, 'boxSetTopLeftPointFunc': True,
    
            # Line Functions
            'lineFunc': True, 'lineCopyFunc': True, 'lineDeleteFunc': True,
            'lineGetPriceFunc': True, 'lineGetX1Func': True, 'lineGetX2Func': True,
            'lineGetY1Func': True, 'lineGetY2Func': True, 'lineNewFunc': True,
            'lineSetColFunc': True, 'lineSetExtendFunc': True, 'lineSetFirstPointFunc': True,
            'lineSetSecondPointFunc': True, 'lineSetStyleFunc': True, 'lineSetWidthFunc': True,
            'lineSetX1Func': True, 'lineSetX2Func': True, 'lineSetXLocFunc': True,
            'lineSetXY1Func': True, 'lineSetXY2Func': True, 'lineSetY1Func': True,
            'lineSetY2Func': True,
    
            # Matrix Functions
            'matrixAddColFunc': True, 'matrixAddRowFunc': True, 'matrixAvgFunc': True,
            'matrixColFunc': True, 'matrixColumnsFunc': True, 'matrixConcatFunc': True,
            'matrixCopyFunc': True, 'matrixDetFunc': True, 'matrixDiffFunc': True,
            'matrixElementsCountFunc': True, 'matrixFillFunc': True, 'matrixGetFunc': True,
            'matrixIsAntiDiagonalFunc': True, 'matrixIsAntiSymmetricFunc': True,
            'matrixIsBinaryFunc': True, 'matrixIsDiagonalFunc': True,
            'matrixIsIdentityFunc': True, 'matrixIsSquareFunc': True,
            'matrixIsStochasticFunc': True, 'matrixIsSymmetricFunc': True,
            'matrixIsTriangularFunc': True, 'matrixIsZeroFunc': True,
            'matrixMaxFunc': True, 'matrixMinFunc': True, 'matrixMultFunc': True,
            'matrixNewTypeFunc': True, 'matrixReshapeFunc': True, 'matrixReverseFunc': True,
            'matrixRowFunc': True, 'matrixRowsFunc': True, 'matrixSetFunc': True,
            'matrixSortFunc': True, 'matrixSumFunc': True, 'matrixTraceFunc': True,
            'matrixTransposeFunc': True,
    
            # String Functions
            'strContains': True, 'strEndsWith': True, 'strFormat': True,
            'strLength': True, 'strLower': True, 'strMatch': True,
            'strPos': True, 'strReplace': True, 'strReplaceAll': True,
            'strSplit': True, 'strStartsWith': True, 'strSubstring': True,
            'strToNumber': True, 'strToString': True, 'strTrim': True,
            'strUpper': True,
    
                    # Chart Functions
            'chartPointCopy': True, 'chartPointFromIndex': True, 'chartPointFromTime': True,
            'chartPointNew': True, 'chartPointNow': True,
    
            # Color Functions
            'colFunc': True, 'colBFunc': True, 'colFromGradientFunc': True,
            'colGFunc': True, 'colNewFunc': True, 'colRFunc': True,
            'colRgbFunc': True, 'colTFunc': True,
    
            # Math Functions
            'mathAbsFunc': True, 'mathAcosFunc': True, 'mathAsinFunc': True,
            'mathAtanFunc': True, 'mathAvgFunc': True, 'mathCeilFunc': True,
            'mathCosFunc': True, 'mathExpFunc': True, 'mathFloorFunc': True,
            'mathLogFunc': True, 'mathLog10Func': True, 'mathMaxFunc': True,
            'mathMinFunc': True, 'mathPowFunc': True, 'mathRandomFunc': True,
            'mathRoundFunc': True, 'mathRoundToMinTickFunc': True, 'mathSignFunc': True,
            'mathSinFunc': True, 'mathSqrtFunc': True, 'mathSumFunc': True,
            'mathTanFunc': True, 'mathToDegreesFunc': True, 'mathToRadiansFunc': True,
    
            # Strategy Functions
            'strategyFunc': True, 'strategyCancelFunc': True, 'strategyCancelAllFunc': True,
            'strategyCloseFunc': True, 'strategyCloseAllFunc': True,
            'strategyEntryFunc': True, 'strategyExitFunc': True,
            'strategyOrderFunc': True,
    
            # Text and Label Functions
            'textAlignBottom': True, 'textAlignCenter': True, 'textAlignLeft': True,
            'textAlignRight': True, 'textAlignTop': True, 'textWrapAuto': True,
            'textWrapNone': True,
    
            # Location Types
            'xLocBarIndex': True, 'xLocBarTime': True, 'yLocAboveBar': True,
            'yLocBelowBar': True, 'yLocPrice': True,
    
            # Data Types
            'Numeric': True, 'Boolean': True, 'String': True, 'Series': True,
    
            # Operators and Keywords
            '=': True, '+': True, '-': True, '*': True, '/': True, '%': True,
            '==': True, '!=': True, '>': True, '<': True, '>=': True, '<=': True,
            'and': True, 'or': True, 'not': True, 'if': True, 'else': True,
            'for': True, 'while': True, 'let': True,
        
                    # Table Functions
            'tableFunc': True, 'tableCellFunc': True, 'tableCellSetBgColFunc': True,
            'tableCellSetHeightFunc': True, 'tableCellSetTextFunc': True,
            'tableCellSetTextColFunc': True, 'tableCellSetTextFontFamily': True,
            'tableCellSetTextHAlignFunc': True, 'tableCellSetTextSizeFunc': True,
            'tableCellSetTextVAlignFunc': True, 'tableCellSetToolTipFunc': True,
            'tableCellSetWidthFunc': True, 'tableClearFunc': True, 'tableDeleteFunc': True,
            'tableMergeCellsFunc': True, 'tableNewFunc': True, 'tableSetBgColFunc': True,
            'tableSetBorderColFunc': True, 'tableSetBorderWidthFunc': True,
            'tableSetFrameColFunc': True, 'tableSetFrameWidthFunc': True,
            'tableSetPositionFunc': True,
    
            # Alert Functions
            'alertFunc': True, 'alertConditionFunc': True,
    
            # Style Functions
            'showStyleArea': True, 'showStyleAreaBr': True, 'showStyleCircles': True,
            'showStyleColumns': True, 'showStyleCross': True, 'showStyleHistogram': True,
            'showStyleLine': True, 'showStyleLineBr': True, 'showStyleStepLine': True,
            'showStyleStepLineDiamond': True, 'showStyleStepLineBr': True,
    
            # Position Functions
            'positionBottomCenter': True, 'positionBottomLeft': True, 'positionBottomRight': True,
            'positionMiddleCenter': True, 'positionMiddleLeft': True, 'positionMiddleRight': True,
            'positionTopCenter': True, 'positionTopLeft': True, 'positionTopRight': True,
    
            # Scale Functions
            'scaleLeft': True, 'scaleNone': True, 'scaleRight': True,
    
            # Session Functions
            'sessionExtended': True, 'sessionRegular': True,
    
            # Settlement Functions
            'settlementAsCloseInherit': True, 'settlementAsCloseOff': True, 'settlementAsCloseOn': True,
    
            # Shape Functions
            'shapeArrowDown': True, 'shapeArrowUp': True, 'shapeCircle': True,
            'shapeCross': True, 'shapeDiamond': True, 'shapeFlag': True,
            'shapeLabelDown': True, 'shapeLabelUp': True, 'shapeSquare': True,
            'shapeTriangleDown': True, 'shapeTriangleUp': True, 'shapeXCross': True,
    
            # Size Functions
            'sizeAuto': True, 'sizeHuge': True, 'sizeLarge': True,
            'sizeNormal': True, 'sizeSmall': True, 'sizeTiny': True,
    
                    # Library and Input Functions
            'libraryFunc': True, 'inputFunc': True, 'inputBoolFunc': True,
            'inputColFunc': True, 'inputEnumFunc': True, 'inputFloatFunc': True,
            'inputIntFunc': True, 'inputPriceFunc': True, 'inputSessionFunc': True,
            'inputSourceFunc': True, 'inputStringFunc': True, 'inputSymbolFunc': True,
            'inputTextAreaFunc': True, 'inputTimeFunc': True, 'inputTimeFrameFunc': True,
    
            # Log Functions
            'logErrorFunc': True, 'logInfoFunc': True, 'logWarningFunc': True,
    
            # Map Functions
            'mapClearFunc': True, 'mapContainsFunc': True, 'mapCopyFunc': True,
            'mapGetFunc': True, 'mapKeysFunc': True, 'mapNewTypeFunc': True,
            'mapPutFunc': True, 'mapPutAllFunc': True, 'mapRemoveFunc': True,
            'mapSizeFunc': True, 'mapValuesFunc': True,
    
            # Request Functions
            'requestCurrencyRateFunc': True, 'requestDividendsFunc': True,
            'requestEarningsFunc': True, 'requestEconomicFunc': True,
            'requestFinancialFunc': True, 'requestQuandlFunc': True,
            'requestSecurityFunc': True, 'requestSecurityLowerTfFunc': True,
            'requestSeedFunc': True, 'requestSplitsFunc': True,
    
            # Runtime Functions
            'runtimeErrorFunc': True,
    
            # Fill Functions
            'fillFunc': True, 'fixNanFunc': True, 'floatFunc': True,
            'hLineFunc': True, 'hourFunc': True, 'indicatorFunc': True,
    
            # Polyline Functions
            'polylineDeleteFunc': True, 'polylineNewFunc': True,
    
                    # Label Functions
            'labelFunc': True, 'labelCopyFunc': True, 'labelDeleteFunc': True,
            'labelGetTextFunc': True, 'labelGetXFunc': True, 'labelGetYFunc': True,
            'labelNewFunc': True, 'labelSetColFunc': True, 'labelSetPointFunc': True,
            'labelSetSizeFunc': True, 'labelSetStyleFunc': True, 'labelSetTextFunc': True,
            'labelSetTextFontFamilyFunc': True, 'labelSetTextAlignFunc': True,
            'labelSetTextColFunc': True, 'labelSetToolTipFunc': True, 'labelSetXFunc': True,
            'labelSetXLocFunc': True, 'labelSetXYFunc': True, 'labelSetYFunc': True,
            'labelSetYLocFunc': True,
    
            # Constants
            'mathE': True, 'mathPhi': True, 'mathPi': True, 'mathRPhi': True,
            'trueValue': True, 'falseValue': True,
    
            # Order Functions
            'orderAscending': True, 'orderDescending': True,
    
            # Bar Functions
            'onTick': True, 'onBar': True,
    
            # Format Functions
            'formatInherit': True, 'formatMinTick': True, 'formatPercent': True,
            'formatPrice': True, 'formatVolume': True,
    
            # Font Functions
            'fontFamilyDefault': True, 'fontFamilyMonospace': True,
    
            # Line Style Functions
            'lineStyleArrowBoth': True, 'lineStyleArrowLeft': True, 'lineStyleArrowRight': True,
            'lineStyleDashed': True, 'lineStyleDotted': True, 'lineStyleSolid': True,
    
            # Location Functions
            'locationAboveBar': True, 'locationAbsolute': True, 'locationBelowBar': True,
            'locationBottom': True, 'locationTop': True,
    
                    # Currency Functions
            'currencyAUD': True, 'currencyBTC': True, 'currencyCAD': True, 'currencyCHF': True,
            'currencyETH': True, 'currencyEUR': True, 'currencyGBP': True, 'currencyHKD': True,
            'currencyINR': True, 'currencyJPY': True, 'currencyKRW': True, 'currencyMYR': True,
            'currencyNOK': True, 'currencyNone': True, 'currencyNZD': True, 'currencyRUB': True,
            'currencySEK': True, 'currencySGD': True, 'currencyTRY': True, 'currencyUSD': True,
            'currencyUSDT': True, 'currencyZAR': True,
    
            # Display Functions
            'displayAll': True, 'displayDataWindow': True, 'displayNone': True,
            'displayPane': True, 'displayPriceScale': True, 'displayStatusLine': True,
    
            # Dividend Functions
            'dividendsGross': True, 'dividendsNet': True,
    
            # Earnings Functions
            'earningsActual': True, 'earningsEstimate': True, 'earningsStandardized': True,
    
            # Extend Functions
            'extendBoth': True, 'extendLeft': True, 'extendNone': True, 'extendRight': True,
    
            # Line Style Functions
            'hlineStyleDashed': True, 'hlineStyleDotted': True, 'hlineStyleSolid': True,
    
            # Label Style Functions
            'labelStyleArrowDown': True, 'labelStyleArrowUp': True, 'labelStyleCircle': True,
            'labelStyleCross': True, 'labelStyleDiamond': True, 'labelStyleFlag': True,
            'labelStyleLabelCenter': True, 'labelStyleLabelDown': True, 'labelStyleLabelLeft': True,
            'labelStyleLabelLowerLeft': True, 'labelStyleLabelLowerRight': True,
            'labelStyleLabelRight': True, 'labelStyleLabelUp': True, 'labelStyleLabelUpperLeft': True,
            'labelStyleLabelUpperRight': True, 'labelStyleNone': True, 'labelStyleSquare': True,
            'labelStyleTextOutline': True, 'labelStyleTriangleDown': True,
            'labelStyleTriangleUp': True, 'labelStyleXCross': True,
    
            # Bar Merge Functions
            'barMergeGapsOff': True, 'barMergeGapsOn': True,
            'barMergeLookaheadOff': True, 'barMergeLookaheadOn': True,
    
            # Adjustment Functions
            'adjustmentDividends': True, 'adjustmentNone': True, 'adjustmentSplits': True,
            'backAdjustmentInherit': True, 'backAdjustmentOff': True, 'backAdjustmentOn': True,
    
                    # Strategy Additional Functions
            'strategyClosedTradesCommissionFunc': True, 'strategyClosedTradesEntryBarIndexFunc': True,
            'strategyClosedTradesEntryCommentFunc': True, 'strategyClosedTradesEntryIdFunc': True,
            'strategyClosedTradesEntryPriceFunc': True, 'strategyClosedTradesEntryTimeFunc': True,
            'strategyClosedTradesExitBarIndexFunc': True, 'strategyClosedTradesExitCommentFunc': True,
            'strategyClosedTradesExitIdFunc': True, 'strategyClosedTradesExitPriceFunc': True,
            'strategyClosedTradesExitTimeFunc': True, 'strategyClosedTradesMaxDrawdownFunc': True,
            'strategyClosedTradesMaxDrawdownPercentFunc': True, 'strategyClosedTradesMaxRunupFunc': True,
            'strategyClosedTradesMaxRunupPercentFunc': True, 'strategyClosedTradesProfitFunc': True,
            'strategyClosedTradesProfitPercentFunc': True, 'strategyClosedTradesSizeFunc': True,
            'strategyConvertToAccountFunc': True, 'strategyConvertToSymbolFunc': True,
            'strategyDefaultEntryQtyFunc': True, 'strategyOpenTradesCommissionFunc': True,
            'strategyOpenTradesEntryBarIndexFunc': True, 'strategyOpenTradesEntryCommentFunc': True,
            'strategyOpenTradesEntryIdFunc': True, 'strategyOpenTradesEntryPriceFunc': True,
            'strategyOpenTradesEntryTimeFunc': True, 'strategyOpenTradesMaxDrawdownFunc': True,
            'strategyOpenTradesMaxDrawdownPercentFunc': True, 'strategyOpenTradesMaxRunupFunc': True,
            'strategyOpenTradesMaxRunupPercentFunc': True, 'strategyOpenTradesProfitFunc': True,
            'strategyOpenTradesProfitPercentFunc': True, 'strategyOpenTradesSizeFunc': True,
            'strategyRiskAllowEntryInFunc': True, 'strategyRiskMaxConsLossDaysFunc': True,
            'strategyRiskMaxDrawdownFunc': True, 'strategyRiskMaxIntradayFilledOrdersFunc': True,
            'strategyRiskMaxIntradayLossFunc': True, 'strategyRiskMaxPositionSizeFunc': True,
    
            # Additional Time Functions
            'timeframeChangeFunc': True, 'timeframeFromSecondsFunc': True,
            'timeframeInSecondsFunc': True, 'timestampFunc': True,
    
            # Show Functions
            'show': True, 'showshape': True, 'showcond': True,
    
            # Line Style Additional
            'solid': True, 'dotted': True, 'dashed': True,

            'AD': True, 'ADOSC': True, 'ADX': True, 'ADXR': True, 'APO': True,
            'AROON': True, 'AROONOSC': True, 'ATR': True, 'AVGPRICE': True, 'BBANDS': True,
            'BETA': True, 'BOP': True, 'CCI': True, 'CDL2CROWS': True, 'CDL3BLACKCROWS': True,
            'CDL3INSIDE': True, 'CDL3LINESTRIKE': True, 'CDL3STARSINSOUTH': True, 'CDL3WHITESOLDIERS': True, 'CDLABANDONEDBABY': True,
            'CDLADVANCEBLOCK': True, 'CDLBELTHOLD': True, 'CDLBREAKAWAY': True, 'CDLCLOSINGMARUBOZU': True, 'CDLCONCEALBABYSWALL': True,
            'CDLCOUNTERATTACK': True, 'CDLDARKCLOUDCOVER': True, 'CDLDOJI': True, 'CDLDOJISTAR': True, 'CDLDRAGONFLYDOJI': True,
            'CDLENGULFING': True, 'CDLEVENINGDOJISTAR': True, 'CDLEVENINGSTAR': True, 'CDLGAPSIDESIDEWHITE': True, 'CDLGRAVESTONEDOJI': True,
            'CDLHAMMER': True, 'CDLHANGINGMAN': True, 'CDLHARAMI': True, 'CDLHARAMICROSS': True, 'CDLHIGHWAVE': True,
            'CDLHIKKAKE': True, 'CDLHIKKAKEMOD': True, 'CDLHOMINGPIGEON': True, 'CDLIDENTICAL3CROWS': True, 'CDLINNECK': True,
            'CDLINVERTEDHAMMER': True, 'CDLKICKING': True, 'CDLKICKINGBYLENGTH': True, 'CDLLADDERBOTTOM': True, 'CDLLONGLEGGEDDOJI': True,
            'CDLLONGLINE': True, 'CDLMARUBOZU': True, 'CDLMATCHINGLOW': True, 'CDLMATHOLD': True, 'CDLMORNINGDOJISTAR': True,
            'CDLMORNINGSTAR': True, 'CDLONNECK': True, 'CDLPIERCING': True, 'CDLRICKSHAWMAN': True, 'CDLRISEFALL3METHODS': True,
            'CDLSEPARATINGLINES': True, 'CDLSHOOTINGSTAR': True, 'CDLSHORTLINE': True, 'CDLSPINNINGTOP': True, 'CDLSTALLEDPATTERN': True,
            'CDLSTICKSANDWICH': True, 'CDLTAKURI': True, 'CDLTASUKIGAP': True, 'CDLTHRUSTING': True, 'CDLTRISTAR': True,
            'CDLUNIQUE3RIVER': True, 'CDLUPSIDEGAP2CROWS': True, 'CDLXSIDEGAP3METHODS': True, 'CMO': True, 'CORREL': True,
            'DEMA': True, 'DX': True, 'EMA': True, 'HT_DCPERIOD': True, 'HT_DCPHASE': True,
            'HT_PHASOR': True, 'HT_SINE': True, 'HT_TRENDLINE': True, 'HT_TRENDMODE': True, 'KAMA': True,
            'LINEARREG': True, 'LINEARREG_ANGLE': True, 'LINEARREG_INTERCEPT': True, 'LINEARREG_SLOPE': True, 'MA': True,
            'MACD': True, 'MACDEXT': True, 'MACDFIX': True, 'MAMA': True, 'MAX': True,
            'MAXINDEX': True, 'MEDPRICE': True, 'MFI': True, 'MIDPOINT': True, 'MIDPRICE': True,
            'MIN': True, 'MININDEX': True, 'MINMAX': True, 'MINMAXINDEX': True, 'MINUS_DI': True,
            'MINUS_DM': True, 'MOM': True, 'NATR': True, 'OBV': True, 'PLUS_DI': True,
            'PLUS_DM': True, 'PPO': True, 'ROC': True, 'ROCP': True, 'ROCR': True,
            'ROCR100': True, 'RSI': True, 'SAR': True, 'SAREXT': True, 'SMA': True,
            'STDDEV': True, 'STOCH': True, 'STOCHF': True, 'STOCHRSI': True, 'SUM': True,
            'T3': True, 'TEMA': True, 'TRANGE': True, 'TRIMA': True, 'TRIX': True,
            'TSF': True, 'TYPPRICE': True, 'ULTOSC': True, 'VAR': True, 'WCLPRICE': True,
            'WILLR': True, 'WMA': True,'CDL2CROWS': True, 'CDL3BLACKCROWS': True, 'CDL3INSIDE': True, 'CDL3LINESTRIKE': True, 'CDL3STARSINSOUTH': True,
            'CDL3WHITESOLDIERS': True, 'CDLABANDONEDBABY': True, 'CDLADVANCEBLOCK': True, 'CDLBELTHOLD': True, 'CDLBREAKAWAY': True,
            'CDLCLOSINGMARUBOZU': True, 'CDLCONCEALBABYSWALL': True, 'CDLCOUNTERATTACK': True, 'CDLDARKCLOUDCOVER': True, 'CDLDOJI': True,
            'CDLDOJISTAR': True, 'CDLDRAGONFLYDOJI': True, 'CDLENGULFING': True, 'CDLEVENINGDOJISTAR': True, 'CDLEVENINGSTAR': True,
            'CDLGAPSIDESIDEWHITE': True, 'CDLGRAVESTONEDOJI': True, 'CDLHAMMER': True, 'CDLHANGINGMAN': True, 'CDLHARAMI': True,
            'CDLHARAMICROSS': True, 'CDLHIGHWAVE': True, 'CDLHIKKAKE': True, 'CDLHIKKAKEMOD': True, 'CDLHOMINGPIGEON': True,
            'CDLIDENTICAL3CROWS': True, 'CDLINNECK': True, 'CDLINVERTEDHAMMER': True, 'CDLKICKING': True, 'CDLKICKINGBYLENGTH': True,
            'CDLLADDERBOTTOM': True, 'CDLLONGLEGGEDDOJI': True, 'CDLLONGLINE': True, 'CDLMARUBOZU': True, 'CDLMATCHINGLOW': True,
            'CDLMATHOLD': True, 'CDLMORNINGDOJISTAR': True, 'CDLMORNINGSTAR': True, 'CDLONNECK': True, 'CDLPIERCING': True,
            'CDLRICKSHAWMAN': True, 'CDLRISEFALL3METHODS': True, 'CDLSEPARATINGLINES': True, 'CDLSHOOTINGSTAR': True, 'CDLSHORTLINE': True,
            'CDLSPINNINGTOP': True, 'CDLSTALLEDPATTERN': True, 'CDLSTICKSANDWICH': True, 'CDLTAKURI': True, 'CDLTASUKIGAP': True,
            'CDLTHRUSTING': True, 'CDLTRISTAR': True, 'CDLUNIQUE3RIVER': True, 'CDLUPSIDEGAP2CROWS': True, 'CDLXSIDEGAP3METHODS': True


    
        }
    
        
    def _initialize_registries(self):
        return {
            'syntax_registry': {
                'elements': self.syntax_list
            }
        }
        
    def execute_calculation(self, syntax_name, *args):
        syntax_info = {
            'name': syntax_name,
            'value': syntax_name
        }
        return self.calculate_syntax(syntax_info, *args)

    calculate_syntax = calculate_syntax

    def update_bar(self, ohlcv):
        self.current_bar = {
            'open': ohlcv['open'],
            'high': ohlcv['high'],
            'low': ohlcv['low'],
            'close': ohlcv['close'],
            'volume': ohlcv['volume'],
            'time': ohlcv['time']
        }
        self.bar_index += 1
        self._update_series()

    def _update_series(self):
        for key in ['open', 'high', 'low', 'close', 'volume']:
            if key not in self.series_data:
                self.series_data[key] = []
            self.series_data[key].append(self.current_bar[key])
            if len(self.series_data[key]) > self.max_bars_back:
                self.series_data[key].pop(0)

    def get_value(self, name, offset=0):
        if name in self.series_data:
            idx = -1 - offset
            if abs(idx) <= len(self.series_data[name]):
                return self.series_data[name][idx]
        return None

    def set_value(self, name, value):
        self.variables[name] = value

        def process_indicator(self, name, *args):
            result = self.execute_calculation(name, *args)
            if name not in self.series_data:
                self.series_data[name] = []
            self.series_data[name].append(result)
            return result

    def get_series(self, name):
        if name in self.series_data:
            return self.series_data[name]
        return []

    def get_bar_state(self):
        return {
            'index': self.bar_index,
            'is_new': True,
            'is_realtime': self.is_realtime,
            'is_confirmed': self.is_confirmed,
            'time': self.current_bar['time'] if self.current_bar else None
        }

    def get_built_in_vars(self):
        if self.current_bar:
            return {
                'open': self.current_bar['open'],
                'high': self.current_bar['high'],
                'low': self.current_bar['low'],
                'close': self.current_bar['close'],
                'volume': self.current_bar['volume'],
                'hl2': (self.current_bar['high'] + self.current_bar['low']) / 2,
                'hlc3': (self.current_bar['high'] + self.current_bar['low'] + self.current_bar['close']) / 3,
                'hlcc4': (self.current_bar['high'] + self.current_bar['low'] + self.current_bar['close'] * 2) / 4,
                'ohlc4': (self.current_bar['open'] + self.current_bar['high'] + self.current_bar['low'] + self.current_bar['close']) / 4
            }
        return {}

    def execute_function(self, name, *args):
        if name in self.registry['syntax_registry']['elements']:
            return self.execute_calculation(name, *args)
        return None

    def process_time_series(self, indicator_name, *args):
            if self.current_bar:
                value = self.execute_calculation(indicator_name, *args)
                if indicator_name not in self.series_data:
                    self.series_data[indicator_name] = []
                self.series_data[indicator_name].append(value)
                return value
            return None

    def get_timeframe_data(self, timeframe):
        if self.current_bar:
            return {
                'time': self.current_bar['time'],
                'open': self.series_data['open'],
                'high': self.series_data['high'],
                'low': self.series_data['low'],
                'close': self.series_data['close'],
                'volume': self.series_data['volume']
            }
        return None

    def process_plot(self, plot_type, value, *args):
        if plot_type in self.registry['syntax_registry']['elements']:
            return self.execute_calculation(plot_type, value, *args)
        return None

    def get_strategy_vars(self):
        return {
            'position_size': self.execute_calculation('strategyPositionSize'),
            'position_avg_price': self.execute_calculation('strategyPositionAvgPrice'),
            'equity': self.execute_calculation('strategyEquity'),
            'net_profit': self.execute_calculation('strategyNetProfit')
        }

    def execute_bar_by_bar(self, script_function):
        if self.current_bar:
            return script_function(self)
        return None

    def process_security(self, symbol, resolution, expression):
        """Handles multi-timeframe analysis like security() function"""
        if self.current_bar:
            return self.execute_calculation(expression)
        return None

    def handle_na(self, value, replacement=None):
        """Handles na values similar to PineScript's na handling"""
        if value is None or math.isnan(value):
            return replacement
        return value

    def process_series_calculation(self, func_name, source, length):
        """Processes rolling calculations like SMA, EMA, RSI"""
        if func_name in self.registry['syntax_registry']['elements']:
            return self.execute_calculation(func_name, source, length)
        return None

    def get_last_values(self, series_name, length):
        """Gets last n values from a series"""
        if series_name in self.series_data:
            return self.series_data[series_name][-length:]
        return []

    def commit_calculation(self, name, value):
        """Commits calculated values to series storage"""
        if name not in self.series_data:
            self.series_data[name] = []
        self.series_data[name].append(value)
        if len(self.series_data[name]) > self.max_bars_back:
            self.series_data[name].pop(0)
    
    def evaluate_code(source_code):
    # Initialize environment
        env = Environment()
    
    # Tokenize the source code
        tokenizer = Tokenizer(source_code)
        tokens = tokenizer.tokenize()

        # Parse tokens
        parser = Parser(tokens)
        syntax = parser.parse_all_syntax()
    
    # Execute calculation using environment
        if syntax:
            result = env.execute_calculation(syntax['name'])
            return result
        return None

    def run_script(code):
        result = evaluate_code(code)
        return result


"""-----------------------------------------------------------------------------------------------------------"""

def evaluate_code(source_code):
    # Initialize environment
    env = Environment()
    
    # Tokenize the source code
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    
    # Parse tokens
    parser = Parser(tokens)
    syntax = parser.parse_all_syntax()
    
    # Execute calculation using environment
    if syntax:
        result = env.execute_calculation(syntax['name'])
        return result
    return None

# Example usage:
def run_script(code):
    result = evaluate_code(code)
    return result



