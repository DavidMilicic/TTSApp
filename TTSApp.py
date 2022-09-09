from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from pygame import mixer, _sdl2 as devices
from configparser import ConfigParser
import pyttsx3
import pygame
import os
import sys
import qdarkstyle

class Ui_TTSApp(QMainWindow):
    def setupUi(self, TTSApp):
        TTSApp.setObjectName("TTSApp")
        TTSApp.resize(670, 275)
        self.centralwidget = QtWidgets.QWidget(TTSApp)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ttsFrame = QtWidgets.QFrame(self.centralwidget)
        self.ttsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ttsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ttsFrame.setObjectName("ttsFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.ttsFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.speakButton = QtWidgets.QPushButton(self.ttsFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.speakButton.setFont(font)
        self.speakButton.setObjectName("speakButton")
        self.gridLayout.addWidget(self.speakButton, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.ttsFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.textInput = QtWidgets.QLineEdit(self.ttsFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textInput.setFont(font)
        self.textInput.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.textInput.setObjectName("textInput")
        self.textInput.returnPressed.connect(self.speakButton.click)
        self.gridLayout.addWidget(self.textInput, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.ttsFrame, 0, 0, 1, 1)

        #voice, output, volume
        self.voiceIOFrame = QtWidgets.QFrame(self.centralwidget)
        self.voiceIOFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.voiceIOFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.voiceIOFrame.setObjectName("voiceIOFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.voiceIOFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(325, 419, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 6, 1, 1, 1)
        self.voiceLabel = QtWidgets.QLabel(self.voiceIOFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.voiceLabel.setFont(font)
        self.voiceLabel.setObjectName("voiceLabel")
        self.gridLayout_2.addWidget(self.voiceLabel, 0, 0, 1, 1)
        self.outputLabel = QtWidgets.QLabel(self.voiceIOFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outputLabel.setFont(font)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout_2.addWidget(self.outputLabel, 2, 0, 1, 1)
        self.outputBox = QtWidgets.QComboBox(self.voiceIOFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outputBox.setFont(font)
        self.outputBox.setObjectName("outputBox")
        self.gridLayout_2.addWidget(self.outputBox, 3, 0, 1, 2)
        self.volumeLabel = QtWidgets.QLabel(self.voiceIOFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.volumeLabel.setFont(font)
        self.volumeLabel.setObjectName("volumeLabel")
        self.gridLayout_2.addWidget(self.volumeLabel, 4, 0, 1, 1)
        self.volumeSlider = QtWidgets.QSlider(self.voiceIOFrame)
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.gridLayout_2.addWidget(self.volumeSlider, 5, 0, 1, 2)
        self.voiceBox = QtWidgets.QComboBox(self.voiceIOFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.voiceBox.setFont(font)
        self.voiceBox.setEditable(False)
        self.voiceBox.setCurrentText("")
        self.voiceBox.setPlaceholderText("")
        self.voiceBox.setObjectName("voiceBox")
        self.gridLayout_2.addWidget(self.voiceBox, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.voiceIOFrame, 0, 1, 1, 1)
        TTSApp.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(TTSApp)
        self.statusbar.setObjectName("statusbar")
        TTSApp.setStatusBar(self.statusbar)

        self.retranslateUi(TTSApp)
        QtCore.QMetaObject.connectSlotsByName(TTSApp)

        #disable speak button
        self.speakButton.setEnabled(False)
        #connect speak button with speak function
        self.speakButton.clicked.connect(self.speak)
        #connect textInput with function to disable speak button if empty | press speak button with enter
        self.textInput.textChanged.connect(self.textState)
        self.textInput.returnPressed.connect(self.speakButton.click)

        #initialize pyttsx3
        self.engine = pyttsx3.init()

        #Get voice names
        self.voices = self.engine.getProperty('voices')
        for voice in self.voices:
                self.voiceBox.addItem(voice.name, voice.id)

        #list of available output devices
        mixer.init()
        for outputDevice in devices.audio.get_audio_device_names(False):
            self.outputBox.addItem(outputDevice)
        mixer.quit()

        #set the config / make a config file if it doesn't exist
        self.config = ConfigParser()
        if os.path.exists("config.ini"):
            pass
        else:
            self.config["output"] = {"device": self.outputBox.currentText()}
            self.config["voices"] = {"voices" : self.voiceBox.currentIndex()}
            self.config["volume"] = {"volume" : self.volumeSlider.value()}
            with open("config.ini", "w") as configfile:
                self.config.write(configfile)

        #read values from config and set them to variables
        self.config.read("config.ini")

        self.outputBox.setCurrentText(self.config.get("output", "device"))
        self.voiceBox.setCurrentIndex(self.config.getint("voices", "voices"))
        self.volumeSlider.setValue(self.config.getint("volume", "volume"))

        self.selectedDevice = self.outputBox.currentText()
        self.selectedVoice = self.voiceBox.currentIndex()
        self.selectedVolume = float(self.volumeSlider.value() / 100)

        #connect components with the functions
        self.outputBox.currentTextChanged.connect(self.outputBoxChanged)
        self.voiceBox.currentIndexChanged.connect(self.voiceChanged)
        self.volumeSlider.valueChanged.connect(self.volumeChanged)

        
    #change config when device/voice/volume has been changed
    def outputBoxChanged(self):
        self.config["output"] = {"device": self.outputBox.currentText()}
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
        self.selectedDevice = self.outputBox.currentText()

    def voiceChanged(self):
        self.config["voices"] = {"voices" : self.voiceBox.currentIndex()}
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
        self.selectedVoice = self.voiceBox.currentIndex()

    def volumeChanged(self):
        self.config["volume"] = {"volume" : self.volumeSlider.value()}
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
        self.selectedVolume = float(self.volumeSlider.value() / 100)

    #check if textInput is empty, prevent user from using speak button if empty
    def textState(self):
        if self.textInput.text() == "":
            self.speakButton.setEnabled(False)
        else:
            self.speakButton.setEnabled(True)
    #TTS
    def speak(self):
        #set voice and volume from config, rate is always 170 because that speed seems good 
        self.engine.setProperty("rate", 170) 
        self.engine.setProperty("voice", self.voices[self.selectedVoice].id)
        self.engine.setProperty("volume", self.selectedVolume)
        self.text = self.textInput.text()
        self.engine.save_to_file(self.text, "speech.wav")
        self.engine.runAndWait()

        #output to selected device, sound loading, playing, sound unloading, removing
        mixer.init(devicename = self.selectedDevice)
        SONG_END = pygame.USEREVENT + 1
        mixer.music.set_endevent(SONG_END)
        mixer.music.load("speech.wav")
        mixer.music.play()
        self.engine.stop()
        pygame.init()
        soundPlaying = True
        while soundPlaying == True:
            #disable text field
            self.textInput.setEnabled(False)
            self.speakButton.setEnabled(False)
            for event in pygame.event.get():
                if event.type == SONG_END:
                    mixer.music.unload()
                    mixer.quit()
                    os.remove("speech.wav")
                    soundPlaying = False
                    #clear text field, enable it, reset focus back to it
                    self.textInput.clear()
                    self.textInput.setEnabled(True)
                    self.textInput.setFocus()

    def retranslateUi(self, TTSApp):
        _translate = QtCore.QCoreApplication.translate
        TTSApp.setWindowTitle(_translate("TTSApp", "TTS App"))
        TTSApp.setWindowIcon(QtGui.QIcon("img/tts.png"))
        self.speakButton.setText(_translate("TTSApp", "Speak"))
        self.label.setText(_translate("TTSApp", "Text-to-Speech"))
        self.voiceLabel.setText(_translate("TTSApp", "Voice"))
        self.outputLabel.setText(_translate("TTSApp", "Output"))
        self.volumeLabel.setText(_translate("TTSApp", "Volume"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    TTSApp = QtWidgets.QMainWindow()
    ui = Ui_TTSApp()
    ui.setupUi(TTSApp)
    TTSApp.show()
    sys.exit(app.exec_())