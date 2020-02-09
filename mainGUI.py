import sys,tkinter
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter.ttk import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

import testy
from PIL import Image, ImageTk
import random

#parameters


#fonts
fontmain = "Verdana 15 bold"
fontbutton = "Verdana 12 bold"
fontoption = "Verdana 10 bold"
fontoption2 = "Verdana 8 bold"

#można też tak: LARGE_FONT = ("Verdana", 12)

#colours
colourtext = "deep pink"
colourbackground = "pink"

#position
#button
positionbutton_x = 50
positionbutton_y = 100
positionbutton_height = 40
positionbutton_width = 200
positiondistancebutton = 50
#rectangle
pos_rec_x = 400
pos_rec_y = 50
pos_rec_h = 400
pos_rec_w = 500
pos_rec_in_dis = 25
pos_rec_in_h = 25
pos_rec_in_w = 150
#result window
res_x = 30
res_y = 0
res_dis = 50
#cord_rec = pos_rec_x, pos_rec_y, pos_rec_x, pos_rec_y + pos_rec_h, pos_rec_x + pos_rec_w, pos_rec_y + pos_rec_h, pos_rec_x + pos_rec_w, pos_rec_y


#tables
ButtonsTestText = ["Test ADC here", "Test DAC here", "Test loopback here"]
ButtonsTest = []
TestingLabelsText = ["frequency[Hz]", "amplitude [Hz]"]#,"Bits","Coding"]
TestingLabels = []
ComboboxTestingDAC = []


#commands
def ADCTest():
    #welcomming.config(state = DISABLED, disabledforeground = welcomming.cget('bg')); -- disabled
    print("You choose ADCTest")
    TestingLabelsText[0] = "frequency [Hz]"
    TestingLabelsText[1] = "amplitude [V]"
    ChangeTextinRectangle()
    EnableRectangle()
    LabelRenameFor("testlabel", "TEST ADC")
    ChangeRangeTo(1, 5, freqsample)
    ADCSolution(True)


def DACTest():
    print("You choose DACTest")
    TestingLabelsText[0] = "frequency [Hz]"
    TestingLabelsText[1] = "amplitude [V]"
    EnableRectangle()
    ChangeTextinRectangle()
    LabelRenameFor("testlabel", "TEST DAC")
    ChangeRangeTo(1, 4, freqsample)
    ADCSolution(False)

def LoopbackTest():
    #welcomming.config(state = DISABLED, disabledforeground = welcomming.cget('bg')); -- disabled
    print("You choose Loopback Test")
    TestingLabelsText[0] = "frequency [Hz]"
    TestingLabelsText[1] = "amplitude [V]" # jakiś parametr
    EnableRectangle()
    ChangeTextinRectangle()
    LabelRenameFor("testlabel", "TEST LOOPBACK")
    ChangeRangeTo(1, 5, freqsample)
    ADCSolution(True)

commands = [ADCTest, DACTest, LoopbackTest]

def GenerateWave():
    print("Generating waveform")
    freq, ampl, waveform,  nametest = FromRectangleParameters()#freq sampling or frequency of sinus/ramp
    #new window with grade and fourier, wave etc.
    #print(freq)
    if(nametest == "TEST DAC"):
        print("TestDac param")
        if waveform == "sinus":
            data, freqs = testy.DAC_test(freq,1)
        if waveform == "ramp":
            data, freqs = testy.DAC_test(freq, 2)
        data_avg = sum(data) / len(data)
        print("DC: " + str(data_avg) + "V")
        print("Signal frequency: " + str(testy.freq_from_fft(data, freqs)) + " Hz")
        print("Sample frequency: " + str(freqs) + " Hz")
    elif(nametest == "TEST ADC"):
        print("Test ADC")
        if waveform  == "sinus":
            data, freqs =  testy.ADC_test(freq,ampl, 1)
        if waveform == "ramp":
            data, freqs = testy.ADC_test(freq, ampl, 2)
        data_avg = sum(data)/len(data)
        print("Zebrana czestotliwosc to: ")
        print(testy.freq_from_fft([i - data_avg for i in data], freqs))
        print("Freqs to: ", freqs)
    elif(nametest == "TEST LOOPBACK"):
        print("nth happend")
    t = np.linspace(0, len(data)*1/freqs, len(data))
    y = data
    NewWindow(freq, testy.freq_from_fft([i - data_avg for i in data], freqs),t,y)

def ViewWave():
    print("I can see waveform i wanna generate")
    freq, amp, waveform, nametest = FromRectangleParameters()
    if (TestName.cget("text") == "TEST DAC"):
        amp = 1
    period = 1 / freq
    sample = 1000
    t = np.linspace(0, period * 3, sample)
    y = []
    if(waveform == "sinus"):
        print("Let's draw sin")
        y = amp*np.sin(2 * np.pi * freq * t)
        Figure(main, t, y,pos_rec_x + 8 * pos_rec_in_dis,pos_rec_y + 2 * pos_rec_in_dis, pos_rec_in_w * 1.8, pos_rec_in_h * 6.2)
    if(waveform == "ramp"):
        print("Lets draw ramp")
        y = amp*signal.sawtooth(2 * np.pi * freq * t)
        Figure(main,t, y,pos_rec_x + 8 * pos_rec_in_dis,pos_rec_y + 2 * pos_rec_in_dis, pos_rec_in_w * 1.8, pos_rec_in_h * 6.2)


def ViewNumber(num):
    res = 10**(int(num)+1)
    LabelRenameFor("freq",str(res))
    print(num)


#main window
main  = tkinter.Tk()
main.geometry("1000x500")
main.config(bg = colourbackground)
main.title("ADC & DAC testing machine")

def GenerateTheBestGrade():
    win = Toplevel(main)
    win.geometry("1000x550")
    win.config(bg=colourbackground)
    win.title("ADC&DAC testing result")
    print("szostka!!!")
    AnDi = Image.open("D:\studia\semestr8\TiN\AnaLDiSc\AD_ocena.png")
    #AnDi = AnDi.resize((300, 150))  ## The (250, 250) is (height, width)
    imAD = ImageTk.PhotoImage(AnDi)
    logoAD = tkinter.Label(win, image=imAD)
    #logoAD.place(x=res_x + 15 * pos_rec_in_dis, y=pos_rec_y + pos_rec_in_dis * 12)
    logoAD.pack()
    win.mainloop()
welcomming = tkinter.Label(main, text = "testing",justify = tkinter.CENTER)
welcomming.config(padx = 10, bg = colourbackground, fg = colourtext, font = fontmain)
welcomming.place(x = 0, y = 0, width = 300, height = 50)

#buttons
for converter in ButtonsTestText:
    iter = ButtonsTestText.index(converter)
    print(iter)
    print(converter)
    ButtonsTest.append(tkinter.Button(main, text = converter))## ,command = ADCTest))
    ButtonsTest[iter].config( bg = colourbackground, fg = colourtext, font = fontbutton)
    ButtonsTest[iter].place(x = positionbutton_x, y = positionbutton_y  + iter * positiondistancebutton, width = positionbutton_width, height = positionbutton_height )
for command in commands:
    iter = commands.index(command)
    ButtonsTest[iter].config(command = command)
ButtonsTest[0].config(command = ADCTest)
ButtonsTest[2].config(state = DISABLED)


image = Image.open("pobrane.png")
image = image.resize((50, 50), Image.ANTIALIAS) ## The (250, 250) is (height, width)
im = ImageTk.PhotoImage(image)
logo = tkinter.Label(main, image = im)
logo.place(x = positionbutton_x + positionbutton_width *0.35, y =  positionbutton_y + 3* positiondistancebutton )



premium = tkinter.Label(main, text ="Comming soon...!" )
premium.config(bg=colourbackground, fg=colourtext, font=fontbutton)
premium.place(x=positionbutton_x, y=positionbutton_y + 4 * positiondistancebutton,
                        width=positionbutton_width, height=positionbutton_height)

#rectangle
rectangle = tkinter.Canvas(main, bg = colourbackground, bd = 5, height=pos_rec_h, width=pos_rec_w, relief =  'ridge',highlightcolor = colourtext)
rectangle.place(x = pos_rec_x, y = pos_rec_y, width = pos_rec_w, height = pos_rec_h)

## inside rectangle

# wave = tkinter.Spinbox(main, values=("sinus", "ramp"), bg = colourbackground, fg = colourtext, font = fontoption, state = DISABLED)
# wave.place(x = pos_rec_x + pos_rec_in_dis , y = pos_rec_y + pos_rec_in_dis, width = pos_rec_in_w , height = pos_rec_in_h)

TestName = tkinter.Label(main, text = "X")
TestName.config(bg=colourbackground, fg=colourtext, font=fontbutton,state = DISABLED)
TestName.place(x = pos_rec_x + pos_rec_in_dis , y = pos_rec_y + pos_rec_in_dis, width = pos_rec_in_w , height = pos_rec_in_h)

wave  = Combobox(main)
wave["values"] = ("sinus", "ramp")
wave.config( foreground = colourtext, font = fontoption, state = DISABLED)
wave.current(0)
wave.place(x = pos_rec_x + pos_rec_in_dis , y = pos_rec_y + pos_rec_in_dis *2, width = pos_rec_in_w , height = pos_rec_in_h)

generatebutton = tkinter.Button(main, text = "Generate", command = GenerateWave)
generatebutton.config(bg=colourbackground, fg=colourtext, font=fontbutton,state = DISABLED)
generatebutton.place(x = pos_rec_x + 10 * pos_rec_in_dis , y = pos_rec_y - 3*pos_rec_in_dis + pos_rec_h, width = pos_rec_in_w , height = pos_rec_in_h)
#pos_rec_x + 8 * pos_rec_in_dis,pos_rec_y + 2 * pos_rec_in_dis, pos_rec_in_w * 1.8, pos_rec_in_h * 6.2

generatebutton1 = tkinter.Button(main, text = "", bd = 0, command = GenerateTheBestGrade)
generatebutton1.config(bg=colourbackground, fg=colourtext, font=fontbutton,state = NORMAL)
generatebutton1.place(x = pos_rec_x + 16 * pos_rec_in_dis , y = pos_rec_y - 3*pos_rec_in_dis + pos_rec_h, width = 20 , height = pos_rec_in_h)


for text in TestingLabelsText:
    iter = TestingLabelsText.index(text)
    TestingLabels.append(tkinter.Label(main, text = text,justify = tkinter.RIGHT))
    TestingLabels[iter].config(padx = 10, bg = colourbackground, fg = colourtext, font = fontoption,state = DISABLED)
    TestingLabels[iter].place(x = pos_rec_x + pos_rec_in_dis , y = pos_rec_y + (3*(iter)+3)*pos_rec_in_dis , width = pos_rec_in_w , height = pos_rec_in_h)


#res = ResolutionSet(numofsamp.get())
#numofsamp.config(resolution =  res)
freqsample = tkinter.Scale(main, width = 15, borderwidth = 2,sliderlength = 25)
freqsample.config(from_ = 1, to = 5, state = DISABLED, bg = colourbackground, fg = colourtext, showvalue = 0 ,font = fontoption2,orient=tkinter.HORIZONTAL, command = ViewNumber, label = "sth", variable = IntVar() )
freqsample.place(x = pos_rec_x + pos_rec_in_dis , y = pos_rec_y + 4*pos_rec_in_dis, width = pos_rec_in_w , height = pos_rec_in_h* 2)

amplitude = tkinter.Scale(main, width = 15, borderwidth = 2,sliderlength = 25)
amplitude.config(from_ = 0, to = 2.5, resolution = 0.25, state = DISABLED, bg = colourbackground, fg = colourtext, showvalue = 1 ,font = fontoption2,orient=tkinter.HORIZONTAL)
amplitude.place(x = pos_rec_x + pos_rec_in_dis , y = pos_rec_y + 7*pos_rec_in_dis, width = pos_rec_in_w , height = 2*pos_rec_in_h)


viewbutton = tkinter.Button(main, text = "View waveform", command = ViewWave)
viewbutton.config(bg=colourbackground, fg=colourtext, font=fontbutton,state = DISABLED)
viewbutton.place(x = pos_rec_x + 10*pos_rec_in_dis , y = pos_rec_y  + pos_rec_in_dis* 9, width = pos_rec_in_w , height = pos_rec_in_h)

view = tkinter.Label(main, text="View: ", font= fontoption)
view.config(bg=colourbackground, fg=colourtext,state = DISABLED)
view.place(x = pos_rec_x +10*pos_rec_in_dis, y = pos_rec_y + pos_rec_in_dis, width = pos_rec_in_w, height = pos_rec_in_h )

#plot

def Figure(main_, x,y, x_pos, y_pos, width, height):
    Fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=75)
    FigSubPlot = Fig.add_subplot(111)
    line1, = FigSubPlot.plot(x,y,"m-")
    canvas = FigureCanvasTkAgg(Fig, main_)
    #canvas.get_tk_widget().place(x = pos_rec_x + 8*pos_rec_in_dis, y = pos_rec_y + 2*pos_rec_in_dis, width = pos_rec_in_w * 1.8, height = pos_rec_in_h*6.2)
    canvas.get_tk_widget().place(x=x_pos, y = y_pos, width = width, height = height)
    canvas.draw()
#Figure(x,y)

#commands
def DisableRectangle():
    amplitude.config(state = DISABLED)
    freqsample.config(state=DISABLED)
    view.config(state=DISABLED)
    for text in TestingLabelsText:
        iter = TestingLabelsText.index(text)
        TestingLabels[iter].config(state=DISABLED)
    generatebutton.config(state = DISABLED)
    wave.config(state=DISABLED)
    viewbutton.config(state=DISABLED)
    TestName.config(state = DISABLED)

def EnableRectangle():
    amplitude.config(state = NORMAL)
    freqsample.config(state=NORMAL)
    view.config(state=NORMAL)
    for text in TestingLabelsText:
        iter = TestingLabelsText.index(text)
        TestingLabels[iter].config(state=NORMAL)
    generatebutton.config(state = NORMAL)
    wave.config(state=NORMAL)
    viewbutton.config(state=NORMAL)
    TestName.config(state=NORMAL)

def ChangeTextinRectangle():
    for text in TestingLabelsText:
        iter = TestingLabelsText.index(text)
        TestingLabels[iter].config(text=text)

def FromRectangleParameters():
    amp = amplitude.get()
    freq = freqsample.get()
    waveform = wave.get()
    nametest = TestName.cget("text")
    print(freq," ",amp)
    print(freq,amp,waveform)
    amp = float(amp)
    freq = int(freq)
    freq = 10**(freq+1)

    return freq, amp, waveform,nametest

def ChangeRangeTo(from_, to, scale ):
    scale.config(from_ = from_, to = to)


def LabelRenameFor(choice, newnamelabel):
    if choice == "freq":
        freqsample.config(label = newnamelabel)
    if choice == "testlabel":
        TestName.config(text = newnamelabel)

def ADCSolution(trueorfalse):
    if trueorfalse == False:
        amplitude.config(state=DISABLED)
        TestingLabels[1].config(state=DISABLED)




def NewWindow(truefreq, freqconverter, t, y):
    print("New Window with result")
    win = Toplevel(main)
    win.geometry("1000x550")
    win.config(bg=colourbackground)
    win.title("ADC&DAC testing result")

    result = tkinter.Label(win, text="RESULT", justify=tkinter.CENTER)
    result.config(padx=10, bg=colourbackground, fg=colourtext, font=fontmain)
    #result.place(x=res_x, y=res_y, width=pos_rec_in_w, height=pos_rec_in_h)
    result.pack()

    freqcheck = tkinter.Label(win, text="Measured frequency = "+str(freqconverter), justify=tkinter.LEFT)
    freqcheck.config(padx=10, bg=colourbackground, fg=colourtext, font=fontoption)
    #freqcheck.place(x=res_x, y=res_y + res_dis, width=pos_rec_in_w, height=pos_rec_in_h)
    freqcheck.pack()
    if(freqconverter > 0.9* truefreq and freqconverter < 1.1* truefreq ):
        freqcheck.config(fg=colourtext)
    else:
        freqcheck.config(fg="red")
    Figure(win, t, y,res_x,pos_rec_y + 1.5 * pos_rec_in_dis , pos_rec_in_w * 6, pos_rec_in_h * 10)

    #grade generating
    randgrade = random.randrange(2,5)


    AnDi = Image.open("D:\studia\semestr8\TiN\AnaLDiSc\AD_ocena ("+str(random.randint(1,6))+").png")
    AnDi = AnDi.resize((300, 150))  ## The (250, 250) is (height, width)
    imAD = ImageTk.PhotoImage(AnDi)
    logoAD = tkinter.Label(win,image=imAD)
    logoAD.place(x = res_x + 15 * pos_rec_in_dis ,y =pos_rec_y + pos_rec_in_dis *12)

    win.mainloop()


def quit():
    main.destroy()
    print("Koniec")
    # hdwf.close()

main.protocol("WM_DELETE_WINDOW", quit)
main. mainloop()

