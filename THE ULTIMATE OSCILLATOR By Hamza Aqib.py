//@version=5
indicator(title="THE ULTIMATE OSCILLATOR, By Hamza Aqib.py", shorttitle="THE ULTIMATE OSCILLATOR, By Hamza Aqib.py", format=format.price, precision=2, timeframe="", timeframe_gaps=true)


ma(source, length, type) =>
    switch type
        "SMA" => ta.sma(source, length)
        "Bollinger Bands" => ta.sma(source, length)
        "EMA" => ta.ema(source, length)
        "SMMA (RMA)" => ta.rma(source, length)
        "WMA" => ta.wma(source, length)
        "VWMA" => ta.vwma(source, length)

rsiLengthInput = input.int(14, minval=1, title="RSI Length", group="RSI Settings")
rsiSourceInput = input.source(close, "Source", group="RSI Settings")
maTypeInput = input.string("SMA", title="MA Type", options=["SMA", "Bollinger Bands", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group="MA Settings")
maLengthInput = input.int(14, title="MA Length", group="MA Settings")
bbMultInput = input.float(2.0, minval=0.001, maxval=50, title="BB StdDev", group="MA Settings")

up = ta.rma(math.max(ta.change(rsiSourceInput), 0), rsiLengthInput)
down = ta.rma(-math.min(ta.change(rsiSourceInput), 0), rsiLengthInput)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
rsiMA = ma(rsi, maLengthInput, maTypeInput)
isBB = maTypeInput == "Bollinger Bands"

rsiPlot = plot(rsi, "RSI", color=#ffffff, style=plot.style_stepline, linewidth=2)
plot(rsiMA, "RSI-based MA", color=color.rgb(0, 225, 255), style=plot.style_stepline, linewidth=2)
rsiUpperBand = hline(70, "RSI Upper Band", color=#00e1ff)
midline = hline(50, "RSI Middle Band", color=color.new(#ff00ea, 50))
rsiLowerBand = hline(30, "RSI Lower Band", color=#00e1ff)
fill(rsiUpperBand, rsiLowerBand, color=color.rgb(126, 87, 194, 90), title="RSI Background Fill")
bbUpperBand = plot(isBB ? rsiMA + ta.stdev(rsi, maLengthInput) * bbMultInput : na, title = "Upper Bollinger Band", color=color.green)
bbLowerBand = plot(isBB ? rsiMA - ta.stdev(rsi, maLengthInput) * bbMultInput : na, title = "Lower Bollinger Band", color=color.green)
fill(bbUpperBand, bbLowerBand, color= isBB ? color.new(color.green, 90) : na, title="Bollinger Bands Background Fill")

midLinePlot = plot(50, color = na, editable = false, display = display.none)
fill(rsiPlot, midLinePlot, 100, 70, title = "Overbought Gradient Fill")
fill(rsiPlot, midLinePlot, 30,  0, title = "Oversold Gradient Fill")

var cumVol = 0.
cumVol += nz(volume)
if barstate.islast and cumVol == 0
    runtime.error("No volume is provided by the data vendor.")
shortlen = input.int(5, minval=1, title = "Short Length")
longlen = input.int(10, minval=1, title = "Long Length")
short = ta.ema(volume, shortlen)
long = ta.ema(volume, longlen)
osc = 1000 * (short - long) / long
hline(50, color = #787B86, title="Zero")
plot(osc, color=#ff0077, style=plot.style_stepline, linewidth = 4)
volUpperBand = hline(320, "VOL Upper Band", color=#787B86)
volmidline = hline(50, "VOL Middle Band", color=color.new(#787B86, 50))
volLowerBand = hline(-272, "VOL Lower Band", color=#787B86)
fill(volUpperBand, volLowerBand, color=color.rgb(38, 0, 255, 90), title="VOL Background Fill")


// Getting inputs
fast_length = input(title="Fast Length", defval=12)
slow_length = input(title="Slow Length", defval=26)
src = input(title="Source", defval=close)
signal_length = input.int(title="Signal Smoothing",  minval = 1, maxval = 50, defval = 9)
sma_source = input.string(title="Oscillator MA Type",  defval="EMA", options=["SMA", "EMA"])
sma_signal = input.string(title="Signal Line MA Type", defval="EMA", options=["SMA", "EMA"])
// Plot colors
col_macd = input(#2962FF, "MACD Line  ", group="Color Settings", inline="MACD")
col_signal = input(#FF6D00, "Signal Line  ", group="Color Settings", inline="Signal")
col_grow_above = input(#26A69A, "Above   Grow", group="Histogram", inline="Above")
col_fall_above = input(#B2DFDB, "Fall", group="Histogram", inline="Above")
col_grow_below = input(#FFCDD2, "Below Grow", group="Histogram", inline="Below")
col_fall_below = input(#FF5252, "Fall", group="Histogram", inline="Below")
// Calculating
fast_ma = sma_source == "SMA" ? ta.sma(src, fast_length) : ta.ema(src, fast_length)
slow_ma = sma_source == "SMA" ? ta.sma(src, slow_length) : ta.ema(src, slow_length)
macd = fast_ma - slow_ma
signal = sma_signal == "SMA" ? ta.sma(macd, signal_length) : ta.ema(macd, signal_length)
hist = macd - signal
hline(50, "Zero Line", color=color.new(#787B86, 50))
plot(hist, title="Histogram", style=plot.style_stepline_diamond, color=(hist>=0 ? (hist[1] < hist ? col_grow_above : col_fall_above) : (hist[1] < hist ? col_grow_below : col_fall_below)))
plot(macd, title="MACD", color=col_macd)
plot(signal, title="Signal", color=col_signal)


