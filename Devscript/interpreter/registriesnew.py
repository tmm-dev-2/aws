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
            }
        }
    }