#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.2.3),
    on December 23, 2025, at 16:02
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware, parallel
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2025.2.3'
expName = 'audiobook_experiment'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1920, 1080]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\User\\repos\\speech-engagement\\engaged_audiobook_experiment\\audiobook_engaged_experiment_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    # initialize 'Realtek'
    deviceManager.addDevice(
        deviceName='Realtek',
        index=4.0,
        name='Realtek HD Audio 2nd output (Realtek(R) Audio)',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        resample=True,
        latencyClass=1,
    )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Instructions" ---
    key_resp_instruction = keyboard.Keyboard(deviceName='defaultKeyboard')
    instruction_text = visual.TextStim(win=win, name='instruction_text',
        text='En el siguiente experimento vas a escuchar dos audiolibros de 5 minutos cada uno.\n\nPor favor, ponete cómodo/a e intenta sostener la mirada en la cruz de fijación que aparecerá en el centro de la pantalla.\n\nCuando estes listo/a apretá ESPACIO: vas a escuchar unos pitidos y luego comenzará el experimento.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "Bips" ---
    # set audio backend
    sound.Sound.backend = 'ptb'
    bip = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Realtek',    name='bip'
    )
    bip.setVolume(1.0)
    polygon = visual.ShapeStim(
        win=win, name='polygon', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='black', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    
    # --- Initialize components for Routine "AudioBook" ---
    audiobook = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=False, 
        speaker='Realtek',    name='audiobook'
    )
    audiobook.setVolume(1.0)
    fixation = visual.ShapeStim(
        win=win, name='fixation', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='black', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    
    # --- Initialize components for Routine "Bips" ---
    bip = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Realtek',    name='bip'
    )
    bip.setVolume(1.0)
    polygon = visual.ShapeStim(
        win=win, name='polygon', vertices='cross',
        size=(0.1, 0.1),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='black', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    
    # --- Initialize components for Routine "Questionary" ---
    end_audiobook1 = keyboard.Keyboard(deviceName='defaultKeyboard')
    question_text = visual.TextStim(win=win, name='question_text',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "SpacebarContinue" ---
    spacebar_response = keyboard.Keyboard(deviceName='defaultKeyboard')
    spacebar_prompt = visual.TextStim(win=win, name='spacebar_prompt',
        text='',
        font='Arial',
        pos=(0, 0.1), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "LastPrompt" ---
    key_resp = keyboard.Keyboard(deviceName='defaultKeyboard')
    last_prompt_text = visual.TextStim(win=win, name='last_prompt_text',
        text='¡Listo! \n\n¿Qué tan largo te pareció el experimento?\n\n\nPresioná un número del 1 al 5 para continuar...',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "GoodBye" ---
    congrats_text = visual.TextStim(win=win, name='congrats_text',
        text='¡Felicitaciones!  \n\nTerminaste el experimento.\n\n\n',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Instructions" ---
    # create an object to store info about Routine Instructions
    Instructions = data.Routine(
        name='Instructions',
        components=[key_resp_instruction, instruction_text],
    )
    Instructions.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_instruction
    key_resp_instruction.keys = []
    key_resp_instruction.rt = []
    _key_resp_instruction_allKeys = []
    # store start times for Instructions
    Instructions.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Instructions.tStart = globalClock.getTime(format='float')
    Instructions.status = STARTED
    thisExp.addData('Instructions.started', Instructions.tStart)
    Instructions.maxDuration = None
    # keep track of which components have finished
    InstructionsComponents = Instructions.components
    for thisComponent in Instructions.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Instructions" ---
    thisExp.currentRoutine = Instructions
    Instructions.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *key_resp_instruction* updates
        waitOnFlip = False
        
        # if key_resp_instruction is starting this frame...
        if key_resp_instruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_instruction.frameNStart = frameN  # exact frame index
            key_resp_instruction.tStart = t  # local t and not account for scr refresh
            key_resp_instruction.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_instruction, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_instruction.started')
            # update status
            key_resp_instruction.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_instruction.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_instruction.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_instruction.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_instruction.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_instruction_allKeys.extend(theseKeys)
            if len(_key_resp_instruction_allKeys):
                key_resp_instruction.keys = _key_resp_instruction_allKeys[-1].name  # just the last key pressed
                key_resp_instruction.rt = _key_resp_instruction_allKeys[-1].rt
                key_resp_instruction.duration = _key_resp_instruction_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *instruction_text* updates
        
        # if instruction_text is starting this frame...
        if instruction_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instruction_text.frameNStart = frameN  # exact frame index
            instruction_text.tStart = t  # local t and not account for scr refresh
            instruction_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instruction_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instruction_text.started')
            # update status
            instruction_text.status = STARTED
            instruction_text.setAutoDraw(True)
        
        # if instruction_text is active this frame...
        if instruction_text.status == STARTED:
            # update params
            pass
        
        # if instruction_text is stopping this frame...
        if instruction_text.status == STARTED:
            if bool(key_resp_instruction.status == FINISHED):
                # keep track of stop time/frame for later
                instruction_text.tStop = t  # not accounting for scr refresh
                instruction_text.tStopRefresh = tThisFlipGlobal  # on global time
                instruction_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instruction_text.stopped')
                # update status
                instruction_text.status = FINISHED
                instruction_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=Instructions,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Instructions.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Instructions.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Instructions.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Instructions" ---
    for thisComponent in Instructions.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Instructions
    Instructions.tStop = globalClock.getTime(format='float')
    Instructions.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Instructions.stopped', Instructions.tStop)
    # check responses
    if key_resp_instruction.keys in ['', [], None]:  # No response was made
        key_resp_instruction.keys = None
    thisExp.addData('key_resp_instruction.keys',key_resp_instruction.keys)
    if key_resp_instruction.keys != None:  # we had a response
        thisExp.addData('key_resp_instruction.rt', key_resp_instruction.rt)
        thisExp.addData('key_resp_instruction.duration', key_resp_instruction.duration)
    thisExp.nextEntry()
    # the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    audiobook_trials = data.TrialHandler2(
        name='audiobook_trials',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('AudioBookLoop.csv'), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(audiobook_trials)  # add the loop to the experiment
    thisAudiobook_trial = audiobook_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisAudiobook_trial.rgb)
    if thisAudiobook_trial != None:
        for paramName in thisAudiobook_trial:
            globals()[paramName] = thisAudiobook_trial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisAudiobook_trial in audiobook_trials:
        audiobook_trials.status = STARTED
        if hasattr(thisAudiobook_trial, 'status'):
            thisAudiobook_trial.status = STARTED
        currentLoop = audiobook_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisAudiobook_trial.rgb)
        if thisAudiobook_trial != None:
            for paramName in thisAudiobook_trial:
                globals()[paramName] = thisAudiobook_trial[paramName]
        
        # set up handler to look after randomisation of conditions etc
        trials_bip1 = data.TrialHandler2(
            name='trials_bip1',
            nReps=10.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
            isTrials=True, 
        )
        thisExp.addLoop(trials_bip1)  # add the loop to the experiment
        thisTrials_bip1 = trials_bip1.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_bip1.rgb)
        if thisTrials_bip1 != None:
            for paramName in thisTrials_bip1:
                globals()[paramName] = thisTrials_bip1[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisTrials_bip1 in trials_bip1:
            trials_bip1.status = STARTED
            if hasattr(thisTrials_bip1, 'status'):
                thisTrials_bip1.status = STARTED
            currentLoop = trials_bip1
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisTrials_bip1.rgb)
            if thisTrials_bip1 != None:
                for paramName in thisTrials_bip1:
                    globals()[paramName] = thisTrials_bip1[paramName]
            
            # --- Prepare to start Routine "Bips" ---
            # create an object to store info about Routine Bips
            Bips = data.Routine(
                name='Bips',
                components=[bip, polygon],
            )
            Bips.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            bip.setSound('../audiobook_stimuli/bip.wav', hamming=True)
            bip.setVolume(1.0, log=False)
            bip.seek(0)
            # store start times for Bips
            Bips.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Bips.tStart = globalClock.getTime(format='float')
            Bips.status = STARTED
            thisExp.addData('Bips.started', Bips.tStart)
            Bips.maxDuration = None
            # keep track of which components have finished
            BipsComponents = Bips.components
            for thisComponent in Bips.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Bips" ---
            thisExp.currentRoutine = Bips
            Bips.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisTrials_bip1, 'status') and thisTrials_bip1.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *bip* updates
                
                # if bip is starting this frame...
                if bip.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    bip.frameNStart = frameN  # exact frame index
                    bip.tStart = t  # local t and not account for scr refresh
                    bip.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('bip.started', tThisFlipGlobal)
                    # update status
                    bip.status = STARTED
                    bip.play(when=win)  # sync with win flip
                
                # if bip is stopping this frame...
                if bip.status == STARTED:
                    if bool(False) or bip.isFinished:
                        # keep track of stop time/frame for later
                        bip.tStop = t  # not accounting for scr refresh
                        bip.tStopRefresh = tThisFlipGlobal  # on global time
                        bip.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'bip.stopped')
                        # update status
                        bip.status = FINISHED
                        bip.stop()
                
                # *polygon* updates
                
                # if polygon is starting this frame...
                if polygon.status == NOT_STARTED and bip.status == STARTED:
                    # keep track of start time/frame for later
                    polygon.frameNStart = frameN  # exact frame index
                    polygon.tStart = t  # local t and not account for scr refresh
                    polygon.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'polygon.started')
                    # update status
                    polygon.status = STARTED
                    polygon.setAutoDraw(True)
                
                # if polygon is active this frame...
                if polygon.status == STARTED:
                    # update params
                    pass
                
                # if polygon is stopping this frame...
                if polygon.status == STARTED:
                    if bool(bip.status == FINISHED):
                        # keep track of stop time/frame for later
                        polygon.tStop = t  # not accounting for scr refresh
                        polygon.tStopRefresh = tThisFlipGlobal  # on global time
                        polygon.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'polygon.stopped')
                        # update status
                        polygon.status = FINISHED
                        polygon.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Bips,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Bips.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Bips.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Bips.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Bips" ---
            for thisComponent in Bips.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Bips
            Bips.tStop = globalClock.getTime(format='float')
            Bips.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Bips.stopped', Bips.tStop)
            bip.pause()  # ensure sound has stopped at end of Routine
            # the Routine "Bips" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisTrials_bip1 as finished
            if hasattr(thisTrials_bip1, 'status'):
                thisTrials_bip1.status = FINISHED
            # if awaiting a pause, pause now
            if trials_bip1.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                trials_bip1.status = STARTED
            thisExp.nextEntry()
            
        # completed 10.0 repeats of 'trials_bip1'
        trials_bip1.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "AudioBook" ---
        # create an object to store info about Routine AudioBook
        AudioBook = data.Routine(
            name='AudioBook',
            components=[audiobook, fixation],
        )
        AudioBook.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        audiobook.setSound(audio_filename, hamming=False)
        audiobook.setVolume(1.0, log=False)
        audiobook.seek(0)
        # store start times for AudioBook
        AudioBook.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        AudioBook.tStart = globalClock.getTime(format='float')
        AudioBook.status = STARTED
        thisExp.addData('AudioBook.started', AudioBook.tStart)
        AudioBook.maxDuration = None
        # keep track of which components have finished
        AudioBookComponents = AudioBook.components
        for thisComponent in AudioBook.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "AudioBook" ---
        thisExp.currentRoutine = AudioBook
        AudioBook.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisAudiobook_trial, 'status') and thisAudiobook_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *audiobook* updates
            
            # if audiobook is starting this frame...
            if audiobook.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                audiobook.frameNStart = frameN  # exact frame index
                audiobook.tStart = t  # local t and not account for scr refresh
                audiobook.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audiobook.started', tThisFlipGlobal)
                # update status
                audiobook.status = STARTED
                audiobook.play(when=win)  # sync with win flip
            
            # if audiobook is stopping this frame...
            if audiobook.status == STARTED:
                if bool(False) or audiobook.isFinished:
                    # keep track of stop time/frame for later
                    audiobook.tStop = t  # not accounting for scr refresh
                    audiobook.tStopRefresh = tThisFlipGlobal  # on global time
                    audiobook.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audiobook.stopped')
                    # update status
                    audiobook.status = FINISHED
                    audiobook.stop()
            
            # *fixation* updates
            
            # if fixation is starting this frame...
            if fixation.status == NOT_STARTED and audiobook.status  == STARTED:
                # keep track of start time/frame for later
                fixation.frameNStart = frameN  # exact frame index
                fixation.tStart = t  # local t and not account for scr refresh
                fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.started')
                # update status
                fixation.status = STARTED
                fixation.setAutoDraw(True)
            
            # if fixation is active this frame...
            if fixation.status == STARTED:
                # update params
                pass
            
            # if fixation is stopping this frame...
            if fixation.status == STARTED:
                if bool(audiobook.status  == FINISHED):
                    # keep track of stop time/frame for later
                    fixation.tStop = t  # not accounting for scr refresh
                    fixation.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fixation.stopped')
                    # update status
                    fixation.status = FINISHED
                    fixation.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=AudioBook,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                AudioBook.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if AudioBook.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in AudioBook.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "AudioBook" ---
        for thisComponent in AudioBook.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for AudioBook
        AudioBook.tStop = globalClock.getTime(format='float')
        AudioBook.tStopRefresh = tThisFlipGlobal
        thisExp.addData('AudioBook.stopped', AudioBook.tStop)
        audiobook.pause()  # ensure sound has stopped at end of Routine
        # the Routine "AudioBook" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        trials_bip2 = data.TrialHandler2(
            name='trials_bip2',
            nReps=10.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
            isTrials=False, 
        )
        thisExp.addLoop(trials_bip2)  # add the loop to the experiment
        thisTrials_bip2 = trials_bip2.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_bip2.rgb)
        if thisTrials_bip2 != None:
            for paramName in thisTrials_bip2:
                globals()[paramName] = thisTrials_bip2[paramName]
        
        for thisTrials_bip2 in trials_bip2:
            trials_bip2.status = STARTED
            if hasattr(thisTrials_bip2, 'status'):
                thisTrials_bip2.status = STARTED
            currentLoop = trials_bip2
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # abbreviate parameter names if possible (e.g. rgb = thisTrials_bip2.rgb)
            if thisTrials_bip2 != None:
                for paramName in thisTrials_bip2:
                    globals()[paramName] = thisTrials_bip2[paramName]
            
            # --- Prepare to start Routine "Bips" ---
            # create an object to store info about Routine Bips
            Bips = data.Routine(
                name='Bips',
                components=[bip, polygon],
            )
            Bips.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            bip.setSound('../audiobook_stimuli/bip.wav', hamming=True)
            bip.setVolume(1.0, log=False)
            bip.seek(0)
            # store start times for Bips
            Bips.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Bips.tStart = globalClock.getTime(format='float')
            Bips.status = STARTED
            thisExp.addData('Bips.started', Bips.tStart)
            Bips.maxDuration = None
            # keep track of which components have finished
            BipsComponents = Bips.components
            for thisComponent in Bips.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Bips" ---
            thisExp.currentRoutine = Bips
            Bips.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisTrials_bip2, 'status') and thisTrials_bip2.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *bip* updates
                
                # if bip is starting this frame...
                if bip.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    bip.frameNStart = frameN  # exact frame index
                    bip.tStart = t  # local t and not account for scr refresh
                    bip.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('bip.started', tThisFlipGlobal)
                    # update status
                    bip.status = STARTED
                    bip.play(when=win)  # sync with win flip
                
                # if bip is stopping this frame...
                if bip.status == STARTED:
                    if bool(False) or bip.isFinished:
                        # keep track of stop time/frame for later
                        bip.tStop = t  # not accounting for scr refresh
                        bip.tStopRefresh = tThisFlipGlobal  # on global time
                        bip.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'bip.stopped')
                        # update status
                        bip.status = FINISHED
                        bip.stop()
                
                # *polygon* updates
                
                # if polygon is starting this frame...
                if polygon.status == NOT_STARTED and bip.status == STARTED:
                    # keep track of start time/frame for later
                    polygon.frameNStart = frameN  # exact frame index
                    polygon.tStart = t  # local t and not account for scr refresh
                    polygon.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(polygon, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'polygon.started')
                    # update status
                    polygon.status = STARTED
                    polygon.setAutoDraw(True)
                
                # if polygon is active this frame...
                if polygon.status == STARTED:
                    # update params
                    pass
                
                # if polygon is stopping this frame...
                if polygon.status == STARTED:
                    if bool(bip.status == FINISHED):
                        # keep track of stop time/frame for later
                        polygon.tStop = t  # not accounting for scr refresh
                        polygon.tStopRefresh = tThisFlipGlobal  # on global time
                        polygon.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'polygon.stopped')
                        # update status
                        polygon.status = FINISHED
                        polygon.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Bips,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Bips.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Bips.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Bips.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Bips" ---
            for thisComponent in Bips.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Bips
            Bips.tStop = globalClock.getTime(format='float')
            Bips.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Bips.stopped', Bips.tStop)
            bip.pause()  # ensure sound has stopped at end of Routine
            # the Routine "Bips" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisTrials_bip2 as finished
            if hasattr(thisTrials_bip2, 'status'):
                thisTrials_bip2.status = FINISHED
            # if awaiting a pause, pause now
            if trials_bip2.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                trials_bip2.status = STARTED
        # completed 10.0 repeats of 'trials_bip2'
        trials_bip2.status = FINISHED
        
        
        # set up handler to look after randomisation of conditions etc
        questionary_loop = data.TrialHandler2(
            name='questionary_loop',
            nReps=3.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
            isTrials=False, 
        )
        thisExp.addLoop(questionary_loop)  # add the loop to the experiment
        thisQuestionary_loop = questionary_loop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisQuestionary_loop.rgb)
        if thisQuestionary_loop != None:
            for paramName in thisQuestionary_loop:
                globals()[paramName] = thisQuestionary_loop[paramName]
        
        for thisQuestionary_loop in questionary_loop:
            questionary_loop.status = STARTED
            if hasattr(thisQuestionary_loop, 'status'):
                thisQuestionary_loop.status = STARTED
            currentLoop = questionary_loop
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            # abbreviate parameter names if possible (e.g. rgb = thisQuestionary_loop.rgb)
            if thisQuestionary_loop != None:
                for paramName in thisQuestionary_loop:
                    globals()[paramName] = thisQuestionary_loop[paramName]
            
            # --- Prepare to start Routine "Questionary" ---
            # create an object to store info about Routine Questionary
            Questionary = data.Routine(
                name='Questionary',
                components=[end_audiobook1, question_text],
            )
            Questionary.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_question
            question_number = questionary_loop.thisN + 1
            print(questionary_loop.nReps)
            if question_number==1:
                question=question1
                answer_a=answer_1_a
                answer_b=answer_1_b
                answer_c=answer_1_c
                correct_answer=correct_answer_1
            elif question_number==2:
                question=question2
                answer_a=answer_2_a
                answer_b=answer_2_b
                answer_c=answer_2_c
                correct_answer=correct_answer_2
            elif question_number==3:
                question=question3
                answer_a=answer_3_a
                answer_b=answer_3_b
                answer_c=answer_3_c
                correct_answer=correct_answer_3
            # create starting attributes for end_audiobook1
            end_audiobook1.keys = []
            end_audiobook1.rt = []
            _end_audiobook1_allKeys = []
            question_text.setText(f"{question}\n\nA) {answer_a}\nB) {answer_b}\nC) {answer_c}\n\nSeleccioná la opción que creas correcta (A, B ó C).")
            # store start times for Questionary
            Questionary.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Questionary.tStart = globalClock.getTime(format='float')
            Questionary.status = STARTED
            thisExp.addData('Questionary.started', Questionary.tStart)
            Questionary.maxDuration = None
            # keep track of which components have finished
            QuestionaryComponents = Questionary.components
            for thisComponent in Questionary.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Questionary" ---
            thisExp.currentRoutine = Questionary
            Questionary.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisQuestionary_loop, 'status') and thisQuestionary_loop.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *end_audiobook1* updates
                waitOnFlip = False
                
                # if end_audiobook1 is starting this frame...
                if end_audiobook1.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                    # keep track of start time/frame for later
                    end_audiobook1.frameNStart = frameN  # exact frame index
                    end_audiobook1.tStart = t  # local t and not account for scr refresh
                    end_audiobook1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(end_audiobook1, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'end_audiobook1.started')
                    # update status
                    end_audiobook1.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(end_audiobook1.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(end_audiobook1.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if end_audiobook1.status == STARTED and not waitOnFlip:
                    theseKeys = end_audiobook1.getKeys(keyList=['a', 'b', 'c'], ignoreKeys=["escape"], waitRelease=False)
                    _end_audiobook1_allKeys.extend(theseKeys)
                    if len(_end_audiobook1_allKeys):
                        end_audiobook1.keys = _end_audiobook1_allKeys[-1].name  # just the last key pressed
                        end_audiobook1.rt = _end_audiobook1_allKeys[-1].rt
                        end_audiobook1.duration = _end_audiobook1_allKeys[-1].duration
                        # a response ends the routine
                        continueRoutine = False
                
                # *question_text* updates
                
                # if question_text is starting this frame...
                if question_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    question_text.frameNStart = frameN  # exact frame index
                    question_text.tStart = t  # local t and not account for scr refresh
                    question_text.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(question_text, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'question_text.started')
                    # update status
                    question_text.status = STARTED
                    question_text.setAutoDraw(True)
                
                # if question_text is active this frame...
                if question_text.status == STARTED:
                    # update params
                    pass
                
                # if question_text is stopping this frame...
                if question_text.status == STARTED:
                    # is it time to stop? (based on local clock)
                    if tThisFlip > end_audiobook1.status == FINISHED-frameTolerance:
                        # keep track of stop time/frame for later
                        question_text.tStop = t  # not accounting for scr refresh
                        question_text.tStopRefresh = tThisFlipGlobal  # on global time
                        question_text.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'question_text.stopped')
                        # update status
                        question_text.status = FINISHED
                        question_text.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Questionary,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Questionary.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Questionary.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Questionary.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Questionary" ---
            for thisComponent in Questionary.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Questionary
            Questionary.tStop = globalClock.getTime(format='float')
            Questionary.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Questionary.stopped', Questionary.tStop)
            # check responses
            if end_audiobook1.keys in ['', [], None]:  # No response was made
                end_audiobook1.keys = None
            questionary_loop.addData('end_audiobook1.keys',end_audiobook1.keys)
            if end_audiobook1.keys != None:  # we had a response
                questionary_loop.addData('end_audiobook1.rt', end_audiobook1.rt)
                questionary_loop.addData('end_audiobook1.duration', end_audiobook1.duration)
            # the Routine "Questionary" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisQuestionary_loop as finished
            if hasattr(thisQuestionary_loop, 'status'):
                thisQuestionary_loop.status = FINISHED
            # if awaiting a pause, pause now
            if questionary_loop.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                questionary_loop.status = STARTED
        # completed 3.0 repeats of 'questionary_loop'
        questionary_loop.status = FINISHED
        
        
        # --- Prepare to start Routine "SpacebarContinue" ---
        # create an object to store info about Routine SpacebarContinue
        SpacebarContinue = data.Routine(
            name='SpacebarContinue',
            components=[spacebar_response, spacebar_prompt],
        )
        SpacebarContinue.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_spacebar
        audiobook_number = audiobook_trials.thisN + 1
        if audiobook_number==len(audiobook_trials.trialList):
            spacebar_text = "Presioná ESPACIO para finalizar"
        else:
            spacebar_text = "Presioná ESPACIO para escuchar la siguiente historia"
        # create starting attributes for spacebar_response
        spacebar_response.keys = []
        spacebar_response.rt = []
        _spacebar_response_allKeys = []
        spacebar_prompt.setText(spacebar_text
        )
        # store start times for SpacebarContinue
        SpacebarContinue.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        SpacebarContinue.tStart = globalClock.getTime(format='float')
        SpacebarContinue.status = STARTED
        thisExp.addData('SpacebarContinue.started', SpacebarContinue.tStart)
        SpacebarContinue.maxDuration = None
        # keep track of which components have finished
        SpacebarContinueComponents = SpacebarContinue.components
        for thisComponent in SpacebarContinue.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "SpacebarContinue" ---
        thisExp.currentRoutine = SpacebarContinue
        SpacebarContinue.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisAudiobook_trial, 'status') and thisAudiobook_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *spacebar_response* updates
            waitOnFlip = False
            
            # if spacebar_response is starting this frame...
            if spacebar_response.status == NOT_STARTED and tThisFlip >= .5-frameTolerance:
                # keep track of start time/frame for later
                spacebar_response.frameNStart = frameN  # exact frame index
                spacebar_response.tStart = t  # local t and not account for scr refresh
                spacebar_response.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(spacebar_response, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'spacebar_response.started')
                # update status
                spacebar_response.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(spacebar_response.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(spacebar_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if spacebar_response.status == STARTED and not waitOnFlip:
                theseKeys = spacebar_response.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _spacebar_response_allKeys.extend(theseKeys)
                if len(_spacebar_response_allKeys):
                    spacebar_response.keys = _spacebar_response_allKeys[-1].name  # just the last key pressed
                    spacebar_response.rt = _spacebar_response_allKeys[-1].rt
                    spacebar_response.duration = _spacebar_response_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *spacebar_prompt* updates
            
            # if spacebar_prompt is starting this frame...
            if spacebar_prompt.status == NOT_STARTED and tThisFlip >= 0.25-frameTolerance:
                # keep track of start time/frame for later
                spacebar_prompt.frameNStart = frameN  # exact frame index
                spacebar_prompt.tStart = t  # local t and not account for scr refresh
                spacebar_prompt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(spacebar_prompt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'spacebar_prompt.started')
                # update status
                spacebar_prompt.status = STARTED
                spacebar_prompt.setAutoDraw(True)
            
            # if spacebar_prompt is active this frame...
            if spacebar_prompt.status == STARTED:
                # update params
                pass
            
            # if spacebar_prompt is stopping this frame...
            if spacebar_prompt.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > spacebar_prompt.tStartRefresh + spacebar_response.status == FINISHED-frameTolerance:
                    # keep track of stop time/frame for later
                    spacebar_prompt.tStop = t  # not accounting for scr refresh
                    spacebar_prompt.tStopRefresh = tThisFlipGlobal  # on global time
                    spacebar_prompt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'spacebar_prompt.stopped')
                    # update status
                    spacebar_prompt.status = FINISHED
                    spacebar_prompt.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=SpacebarContinue,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                SpacebarContinue.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if SpacebarContinue.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in SpacebarContinue.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "SpacebarContinue" ---
        for thisComponent in SpacebarContinue.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for SpacebarContinue
        SpacebarContinue.tStop = globalClock.getTime(format='float')
        SpacebarContinue.tStopRefresh = tThisFlipGlobal
        thisExp.addData('SpacebarContinue.stopped', SpacebarContinue.tStop)
        # check responses
        if spacebar_response.keys in ['', [], None]:  # No response was made
            spacebar_response.keys = None
        audiobook_trials.addData('spacebar_response.keys',spacebar_response.keys)
        if spacebar_response.keys != None:  # we had a response
            audiobook_trials.addData('spacebar_response.rt', spacebar_response.rt)
            audiobook_trials.addData('spacebar_response.duration', spacebar_response.duration)
        # the Routine "SpacebarContinue" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisAudiobook_trial as finished
        if hasattr(thisAudiobook_trial, 'status'):
            thisAudiobook_trial.status = FINISHED
        # if awaiting a pause, pause now
        if audiobook_trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            audiobook_trials.status = STARTED
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'audiobook_trials'
    audiobook_trials.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "LastPrompt" ---
    # create an object to store info about Routine LastPrompt
    LastPrompt = data.Routine(
        name='LastPrompt',
        components=[key_resp, last_prompt_text],
    )
    LastPrompt.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # store start times for LastPrompt
    LastPrompt.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LastPrompt.tStart = globalClock.getTime(format='float')
    LastPrompt.status = STARTED
    thisExp.addData('LastPrompt.started', LastPrompt.tStart)
    LastPrompt.maxDuration = None
    # keep track of which components have finished
    LastPromptComponents = LastPrompt.components
    for thisComponent in LastPrompt.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LastPrompt" ---
    thisExp.currentRoutine = LastPrompt
    LastPrompt.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= .2-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['1','2','3','4','5', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *last_prompt_text* updates
        
        # if last_prompt_text is starting this frame...
        if last_prompt_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            last_prompt_text.frameNStart = frameN  # exact frame index
            last_prompt_text.tStart = t  # local t and not account for scr refresh
            last_prompt_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(last_prompt_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'last_prompt_text.started')
            # update status
            last_prompt_text.status = STARTED
            last_prompt_text.setAutoDraw(True)
        
        # if last_prompt_text is active this frame...
        if last_prompt_text.status == STARTED:
            # update params
            pass
        
        # if last_prompt_text is stopping this frame...
        if last_prompt_text.status == STARTED:
            if bool(key_resp.status == FINISHED):
                # keep track of stop time/frame for later
                last_prompt_text.tStop = t  # not accounting for scr refresh
                last_prompt_text.tStopRefresh = tThisFlipGlobal  # on global time
                last_prompt_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'last_prompt_text.stopped')
                # update status
                last_prompt_text.status = FINISHED
                last_prompt_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=LastPrompt,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            LastPrompt.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if LastPrompt.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in LastPrompt.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LastPrompt" ---
    for thisComponent in LastPrompt.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LastPrompt
    LastPrompt.tStop = globalClock.getTime(format='float')
    LastPrompt.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LastPrompt.stopped', LastPrompt.tStop)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
        thisExp.addData('key_resp.duration', key_resp.duration)
    thisExp.nextEntry()
    # the Routine "LastPrompt" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "GoodBye" ---
    # create an object to store info about Routine GoodBye
    GoodBye = data.Routine(
        name='GoodBye',
        components=[congrats_text],
    )
    GoodBye.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for GoodBye
    GoodBye.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    GoodBye.tStart = globalClock.getTime(format='float')
    GoodBye.status = STARTED
    thisExp.addData('GoodBye.started', GoodBye.tStart)
    GoodBye.maxDuration = None
    # keep track of which components have finished
    GoodByeComponents = GoodBye.components
    for thisComponent in GoodBye.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "GoodBye" ---
    thisExp.currentRoutine = GoodBye
    GoodBye.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 5.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *congrats_text* updates
        
        # if congrats_text is starting this frame...
        if congrats_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            congrats_text.frameNStart = frameN  # exact frame index
            congrats_text.tStart = t  # local t and not account for scr refresh
            congrats_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(congrats_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'congrats_text.started')
            # update status
            congrats_text.status = STARTED
            congrats_text.setAutoDraw(True)
        
        # if congrats_text is active this frame...
        if congrats_text.status == STARTED:
            # update params
            pass
        
        # if congrats_text is stopping this frame...
        if congrats_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > congrats_text.tStartRefresh + 5-frameTolerance:
                # keep track of stop time/frame for later
                congrats_text.tStop = t  # not accounting for scr refresh
                congrats_text.tStopRefresh = tThisFlipGlobal  # on global time
                congrats_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'congrats_text.stopped')
                # update status
                congrats_text.status = FINISHED
                congrats_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=GoodBye,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            GoodBye.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if GoodBye.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in GoodBye.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "GoodBye" ---
    for thisComponent in GoodBye.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for GoodBye
    GoodBye.tStop = globalClock.getTime(format='float')
    GoodBye.tStopRefresh = tThisFlipGlobal
    thisExp.addData('GoodBye.stopped', GoodBye.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if GoodBye.maxDurationReached:
        routineTimer.addTime(-GoodBye.maxDuration)
    elif GoodBye.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-5.000000)
    thisExp.nextEntry()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
