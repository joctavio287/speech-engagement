/***************************** 
 * Audiobook_Experiment *
 *****************************/

import { core, data, sound, util, visual, hardware } from './lib/psychojs-2024.2.4.js';
const { PsychoJS } = core;
const { TrialHandler, MultiStairHandler } = data;
const { Scheduler } = util;
//some handy aliases as in the psychopy scripts;
const { abs, sin, cos, PI: pi, sqrt } = Math;
const { round } = util;


// store info about the experiment session:
let expName = 'audiobook_experiment';  // from the Builder filename that created this script
let expInfo = {
    'participant': `${util.pad(Number.parseFloat(util.randint(0, 999999)).toFixed(0), 6)}`,
    'session': '001',
};

// Start code blocks for 'Before Experiment'
// init psychoJS:
const psychoJS = new PsychoJS({
  debug: true
});

// open window:
psychoJS.openWindow({
  fullscr: true,
  color: new util.Color([0,0,0]),
  units: 'height',
  waitBlanking: true,
  backgroundImage: '',
  backgroundFit: 'none',
});
// schedule the experiment:
psychoJS.schedule(psychoJS.gui.DlgFromDict({
  dictionary: expInfo,
  title: expName
}));

const flowScheduler = new Scheduler(psychoJS);
const dialogCancelScheduler = new Scheduler(psychoJS);
psychoJS.scheduleCondition(function() { return (psychoJS.gui.dialogComponent.button === 'OK'); },flowScheduler, dialogCancelScheduler);

// flowScheduler gets run if the participants presses OK
flowScheduler.add(updateInfo); // add timeStamp
flowScheduler.add(experimentInit);
flowScheduler.add(InstructionsRoutineBegin());
flowScheduler.add(InstructionsRoutineEachFrame());
flowScheduler.add(InstructionsRoutineEnd());
const trialsLoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trialsLoopBegin(trialsLoopScheduler));
flowScheduler.add(trialsLoopScheduler);
flowScheduler.add(trialsLoopEnd);


const trials_2LoopScheduler = new Scheduler(psychoJS);
flowScheduler.add(trials_2LoopBegin(trials_2LoopScheduler));
flowScheduler.add(trials_2LoopScheduler);
flowScheduler.add(trials_2LoopEnd);




flowScheduler.add(LastPromptRoutineBegin());
flowScheduler.add(LastPromptRoutineEachFrame());
flowScheduler.add(LastPromptRoutineEnd());
flowScheduler.add(GoodByeRoutineBegin());
flowScheduler.add(GoodByeRoutineEachFrame());
flowScheduler.add(GoodByeRoutineEnd());
flowScheduler.add(quitPsychoJS, 'Thank you for your patience.', true);

// quit if user presses Cancel in dialog box:
dialogCancelScheduler.add(quitPsychoJS, 'Thank you for your patience.', false);

psychoJS.start({
  expName: expName,
  expInfo: expInfo,
  resources: [
    // resources:
    {'name': 'AudiobookLoop.xlsx', 'path': 'AudiobookLoop.xlsx'},
    {'name': '../data/stimuli_audiobook/audio01.wav', 'path': '../data/stimuli_audiobook/audio01.wav'},
    {'name': '../data/stimuli_audiobook/audio02.wav', 'path': '../data/stimuli_audiobook/audio02.wav'},
    {'name': '..\data\stimuli_audiobook\bip.wav', 'path': '../data/stimuli_audiobook/bip.wav'},
  ]
});

psychoJS.experimentLogger.setLevel(core.Logger.ServerLevel.INFO);

async function updateInfo() {
  currentLoop = psychoJS.experiment;  // right now there are no loops
  expInfo['date'] = util.MonotonicClock.getDateStr();  // add a simple timestamp
  expInfo['expName'] = expName;
  expInfo['psychopyVersion'] = '2024.2.4';
  expInfo['OS'] = window.navigator.platform;


  // store frame rate of monitor if we can measure it successfully
  expInfo['frameRate'] = psychoJS.window.getActualFrameRate();
  if (typeof expInfo['frameRate'] !== 'undefined')
    frameDur = 1.0 / Math.round(expInfo['frameRate']);
  else
    frameDur = 1.0 / 60.0; // couldn't get a reliable measure so guess

  // add info from the URL:
  util.addInfoFromUrl(expInfo);
  

  
  psychoJS.experiment.dataFileName = (("." + "/") + `data/${expInfo["participant"]}_${expName}_${expInfo["date"]}`);
  psychoJS.experiment.field_separator = '\t';


  return Scheduler.Event.NEXT;
}

async function experimentInit() {
  // Initialize components for Routine "Instructions"
  InstructionsClock = new util.Clock();
  instruction_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'instruction_text',
    text: 'En el siguiente experimento vas a escuchar dos audiolibros de 5 minutos cada uno. \n\nPor favor, ponete cómodo/a e intenta sostener la mirada en la cruz de fijación que aparecerá en el centro de la pantalla durante cada cuento.\n\nCuando estes listo/a apretá la barra espaciadora, vas a escuchar unos pitidos y luego comenzará el experimento.',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  key_resp_instruction = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "Bips"
  BipsClock = new util.Clock();
  pip = new sound.Sound({
      win: psychoJS.window,
      value: 'A',
      secs: 1,
      });
  pip.setVolume(1.0);
  polygon = new visual.ShapeStim ({
    win: psychoJS.window, name: 'polygon', 
    vertices: [[-[0.5, 0.5][0]/2.0, -[0.5, 0.5][1]/2.0], [+[0.5, 0.5][0]/2.0, -[0.5, 0.5][1]/2.0], [0, [0.5, 0.5][1]/2.0]],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -1, 
    interpolate: true, 
  });
  
  // Initialize components for Routine "AudioBook"
  AudioBookClock = new util.Clock();
  audiobook = new sound.Sound({
      win: psychoJS.window,
      value: 'A',
      secs: (- 1),
      });
  audiobook.setVolume(1.0);
  fixation = new visual.ShapeStim ({
    win: psychoJS.window, name: 'fixation', 
    vertices: 'cross', size:[0.1, 0.1],
    ori: 0.0, 
    pos: [0, 0], 
    draggable: false, 
    anchor: 'center', 
    lineWidth: 1.0, 
    lineColor: new util.Color('white'), 
    fillColor: new util.Color('white'), 
    colorSpace: 'rgb', 
    opacity: undefined, 
    depth: -1, 
    interpolate: true, 
  });
  
  // Initialize components for Routine "Question"
  QuestionClock = new util.Clock();
  question = new visual.TextStim({
    win: psychoJS.window,
    name: 'question',
    text: '',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0.2], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  answer = new visual.TextBox({
    win: psychoJS.window,
    name: 'answer',
    text: '',
    placeholder: 'Escribí con el teclado tu respuesta. La misma no debe durar más de dos oraciones [...]',
    font: 'Arial',
    pos: [0, (- 0.2)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: undefined, borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: true,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: true,
    multiline: true,
    anchor: 'center',
    depth: -1.0 
  });
  
  end_audiobook1 = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "SpacebarContinue"
  SpacebarContinueClock = new util.Clock();
  spacebar_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'spacebar_text',
    text: 'Apreta la barra espaciadora para continuar  con el segundo cuento [...]',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  spacebar_response = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "LastPrompt"
  LastPromptClock = new util.Clock();
  last_prompt_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'last_prompt_text',
    text: '¡Listo! \n\nDel 1 al 5, ¿qué tan largo te pareció el experimento?\n',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0.2], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  rating_response = new visual.TextBox({
    win: psychoJS.window,
    name: 'rating_response',
    text: '',
    placeholder: 'Apretá un número del 1 al 5',
    font: 'Arial',
    pos: [0, (- 0.2)], 
    draggable: false,
    letterHeight: 0.05,
    lineSpacing: 1.0,
    size: [0.5, 0.5],  units: undefined, 
    ori: 0.0,
    color: 'white', colorSpace: 'rgb',
    fillColor: undefined, borderColor: undefined,
    languageStyle: 'LTR',
    bold: false, italic: false,
    opacity: undefined,
    padding: 0.0,
    alignment: 'center',
    overflow: 'visible',
    editable: true,
    multiline: true,
    anchor: 'center',
    depth: -1.0 
  });
  
  key_resp = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Initialize components for Routine "GoodBye"
  GoodByeClock = new util.Clock();
  congrats_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'congrats_text',
    text: '¡Felicitaciones! \n\nTerminaste el experimento\n',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: 0.0 
  });
  
  press_bar_text = new visual.TextStim({
    win: psychoJS.window,
    name: 'press_bar_text',
    text: '\nApretá la barra espaciadora para finalizar el experimento...\n',
    font: 'Arial',
    units: undefined, 
    pos: [0, 0], draggable: false, height: 0.05,  wrapWidth: undefined, ori: 0.0,
    languageStyle: 'LTR',
    color: new util.Color('white'),  opacity: undefined,
    depth: -1.0 
  });
  
  key_resp_end = new core.Keyboard({psychoJS: psychoJS, clock: new util.Clock(), waitForStart: true});
  
  // Create some handy timers
  globalClock = new util.Clock();  // to track the time since experiment started
  routineTimer = new util.CountdownTimer();  // to track time remaining of each (non-slip) routine
  
  return Scheduler.Event.NEXT;
}

function InstructionsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'Instructions' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    InstructionsClock.reset();
    routineTimer.reset();
    InstructionsMaxDurationReached = false;
    // update component parameters for each repeat
    key_resp_instruction.keys = undefined;
    key_resp_instruction.rt = undefined;
    _key_resp_instruction_allKeys = [];
    psychoJS.experiment.addData('Instructions.started', globalClock.getTime());
    InstructionsMaxDuration = null
    // keep track of which components have finished
    InstructionsComponents = [];
    InstructionsComponents.push(instruction_text);
    InstructionsComponents.push(key_resp_instruction);
    
    for (const thisComponent of InstructionsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function InstructionsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'Instructions' ---
    // get current time
    t = InstructionsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    
    // *instruction_text* updates
    if (t >= 0.0 && instruction_text.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      instruction_text.tStart = t;  // (not accounting for frame time here)
      instruction_text.frameNStart = frameN;  // exact frame index
      
      instruction_text.setAutoDraw(true);
    }
    
    
    // *key_resp_instruction* updates
    if (t >= 0.0 && key_resp_instruction.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      key_resp_instruction.tStart = t;  // (not accounting for frame time here)
      key_resp_instruction.frameNStart = frameN;  // exact frame index
      
      // keyboard checking is just starting
      psychoJS.window.callOnFlip(function() { key_resp_instruction.clock.reset(); });  // t=0 on next screen flip
      psychoJS.window.callOnFlip(function() { key_resp_instruction.start(); }); // start on screen flip
      psychoJS.window.callOnFlip(function() { key_resp_instruction.clearEvents(); });
    }
    
    if (key_resp_instruction.status === PsychoJS.Status.STARTED) {
      let theseKeys = key_resp_instruction.getKeys({keyList: ['space'], waitRelease: false});
      _key_resp_instruction_allKeys = _key_resp_instruction_allKeys.concat(theseKeys);
      if (_key_resp_instruction_allKeys.length > 0) {
        key_resp_instruction.keys = _key_resp_instruction_allKeys[_key_resp_instruction_allKeys.length - 1].name;  // just the last key pressed
        key_resp_instruction.rt = _key_resp_instruction_allKeys[_key_resp_instruction_allKeys.length - 1].rt;
        key_resp_instruction.duration = _key_resp_instruction_allKeys[_key_resp_instruction_allKeys.length - 1].duration;
        // a response ends the routine
        continueRoutine = false;
      }
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of InstructionsComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function InstructionsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'Instructions' ---
    for (const thisComponent of InstructionsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('Instructions.stopped', globalClock.getTime());
    // update the trial handler
    if (currentLoop instanceof MultiStairHandler) {
      currentLoop.addResponse(key_resp_instruction.corr, level);
    }
    psychoJS.experiment.addData('key_resp_instruction.keys', key_resp_instruction.keys);
    if (typeof key_resp_instruction.keys !== 'undefined') {  // we had a response
        psychoJS.experiment.addData('key_resp_instruction.rt', key_resp_instruction.rt);
        psychoJS.experiment.addData('key_resp_instruction.duration', key_resp_instruction.duration);
        routineTimer.reset();
        }
    
    key_resp_instruction.stop();
    // the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset();
    
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function trialsLoopBegin(trialsLoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 20, method: TrialHandler.Method.RANDOM,
      extraInfo: expInfo, originPath: undefined,
      trialList: undefined,
      seed: undefined, name: 'trials'
    });
    psychoJS.experiment.addLoop(trials); // add the loop to the experiment
    currentLoop = trials;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial of trials) {
      snapshot = trials.getSnapshot();
      trialsLoopScheduler.add(importConditions(snapshot));
      trialsLoopScheduler.add(BipsRoutineBegin(snapshot));
      trialsLoopScheduler.add(BipsRoutineEachFrame());
      trialsLoopScheduler.add(BipsRoutineEnd(snapshot));
      trialsLoopScheduler.add(trialsLoopEndIteration(trialsLoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}

async function trialsLoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(trials);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}

function trialsLoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}

function trials_2LoopBegin(trials_2LoopScheduler, snapshot) {
  return async function() {
    TrialHandler.fromSnapshot(snapshot); // update internal variables (.thisN etc) of the loop
    
    // set up handler to look after randomisation of conditions etc
    trials_2 = new TrialHandler({
      psychoJS: psychoJS,
      nReps: 1, method: TrialHandler.Method.SEQUENTIAL,
      extraInfo: expInfo, originPath: undefined,
      trialList: 'AudiobookLoop.xlsx',
      seed: undefined, name: 'trials_2'
    });
    psychoJS.experiment.addLoop(trials_2); // add the loop to the experiment
    currentLoop = trials_2;  // we're now the current loop
    
    // Schedule all the trials in the trialList:
    for (const thisTrial_2 of trials_2) {
      snapshot = trials_2.getSnapshot();
      trials_2LoopScheduler.add(importConditions(snapshot));
      trials_2LoopScheduler.add(AudioBookRoutineBegin(snapshot));
      trials_2LoopScheduler.add(AudioBookRoutineEachFrame());
      trials_2LoopScheduler.add(AudioBookRoutineEnd(snapshot));
      trials_2LoopScheduler.add(QuestionRoutineBegin(snapshot));
      trials_2LoopScheduler.add(QuestionRoutineEachFrame());
      trials_2LoopScheduler.add(QuestionRoutineEnd(snapshot));
      trials_2LoopScheduler.add(SpacebarContinueRoutineBegin(snapshot));
      trials_2LoopScheduler.add(SpacebarContinueRoutineEachFrame());
      trials_2LoopScheduler.add(SpacebarContinueRoutineEnd(snapshot));
      trials_2LoopScheduler.add(trials_2LoopEndIteration(trials_2LoopScheduler, snapshot));
    }
    
    return Scheduler.Event.NEXT;
  }
}

async function trials_2LoopEnd() {
  // terminate loop
  psychoJS.experiment.removeLoop(trials_2);
  // update the current loop from the ExperimentHandler
  if (psychoJS.experiment._unfinishedLoops.length>0)
    currentLoop = psychoJS.experiment._unfinishedLoops.at(-1);
  else
    currentLoop = psychoJS.experiment;  // so we use addData from the experiment
  return Scheduler.Event.NEXT;
}

function trials_2LoopEndIteration(scheduler, snapshot) {
  // ------Prepare for next entry------
  return async function () {
    if (typeof snapshot !== 'undefined') {
      // ------Check if user ended loop early------
      if (snapshot.finished) {
        // Check for and save orphaned data
        if (psychoJS.experiment.isEntryEmpty()) {
          psychoJS.experiment.nextEntry(snapshot);
        }
        scheduler.stop();
      } else {
        psychoJS.experiment.nextEntry(snapshot);
      }
    return Scheduler.Event.NEXT;
    }
  };
}

function BipsRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'Bips' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    BipsClock.reset(routineTimer.getTime());
    routineTimer.add(1.000000);
    BipsMaxDurationReached = false;
    // update component parameters for each repeat
    pip.setValue('C:/Users/User/repos/Speech-engagement/data/stimuli_audiobook/bip.wav');
    pip.secs=1;
    pip.setVolume(1.0);
    psychoJS.experiment.addData('Bips.started', globalClock.getTime());
    BipsMaxDuration = null
    // keep track of which components have finished
    BipsComponents = [];
    BipsComponents.push(pip);
    BipsComponents.push(polygon);
    
    for (const thisComponent of BipsComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function BipsRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'Bips' ---
    // get current time
    t = BipsClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    // start/stop pip
    if (t >= 0.0 && pip.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      pip.tStart = t;  // (not accounting for frame time here)
      pip.frameNStart = frameN;  // exact frame index
      
      psychoJS.window.callOnFlip(function(){ pip.play(); });  // screen flip
      pip.status = PsychoJS.Status.STARTED;
    }
    frameRemains = 0.0 + 1 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (pip.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      if (t >= pip.tStart + 0.5) {
        pip.stop();  // stop the sound (if longer than duration)
        pip.status = PsychoJS.Status.FINISHED;
      }
    }
    
    // *polygon* updates
    if (t >= 0.0 && polygon.status === PsychoJS.Status.NOT_STARTED) {
      // keep track of start time/frame for later
      polygon.tStart = t;  // (not accounting for frame time here)
      polygon.frameNStart = frameN;  // exact frame index
      
      polygon.setAutoDraw(true);
    }
    
    frameRemains = 0.0 + 1.0 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
    if (polygon.status === PsychoJS.Status.STARTED && t >= frameRemains) {
      polygon.setAutoDraw(false);
    }
    
    // check for quit (typically the Esc key)
    if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
      return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
    }
    
    // check if the Routine should terminate
    if (!continueRoutine) {  // a component has requested a forced-end of Routine
      return Scheduler.Event.NEXT;
    }
    
    continueRoutine = false;  // reverts to True if at least one component still running
    for (const thisComponent of BipsComponents)
      if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
        continueRoutine = true;
        break;
      }
    
    // refresh the screen if continuing
    if (continueRoutine && routineTimer.getTime() > 0) {
      return Scheduler.Event.FLIP_REPEAT;
    } else {
      return Scheduler.Event.NEXT;
    }
  };
}

function BipsRoutineEnd(snapshot) {
  return async function () {
    //--- Ending Routine 'Bips' ---
    for (const thisComponent of BipsComponents) {
      if (typeof thisComponent.setAutoDraw === 'function') {
        thisComponent.setAutoDraw(false);
      }
    }
    psychoJS.experiment.addData('Bips.stopped', globalClock.getTime());
    pip.stop();  // ensure sound has stopped at end of Routine
    if (BipsMaxDurationReached) {
        BipsClock.add(BipsMaxDuration);
    } else {
        BipsClock.add(1.000000);
    }
    // Routines running outside a loop should always advance the datafile row
    if (currentLoop === psychoJS.experiment) {
      psychoJS.experiment.nextEntry(snapshot);
    }
    return Scheduler.Event.NEXT;
  }
}

function AudioBookRoutineBegin(snapshot) {
  return async function () {
    TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
    
    //--- Prepare to start Routine 'AudioBook' ---
    t = 0;
    frameN = -1;
    continueRoutine = true; // until we're told otherwise
    AudioBookClock.reset();
    routineTimer.reset();
    AudioBookMaxDurationReached = false;
    // update component parameters for each repeat
    audiobook.setValue(audiofile);
    audiobook.setVolume(1.0);
    psychoJS.experiment.addData('AudioBook.started', globalClock.getTime());
    AudioBookMaxDuration = null
    // keep track of which components have finished
    AudioBookComponents = [];
    AudioBookComponents.push(audiobook);
    AudioBookComponents.push(fixation);
    
    for (const thisComponent of AudioBookComponents)
      if ('status' in thisComponent)
        thisComponent.status = PsychoJS.Status.NOT_STARTED;
    return Scheduler.Event.NEXT;
  }
}

function AudioBookRoutineEachFrame() {
  return async function () {
    //--- Loop for each frame of Routine 'AudioBook' ---
    // get current time
    t = AudioBookClock.getTime();
    frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
    // update/draw components on each frame
    // start/stop audiobook
    psychoJS.window.callOnFlip(function(){ audiobook.play(); });  // screen flip
    audiobook.status = PsychoJS.Status.STARTED;
  }
  if (t >= (audiobook.getDuration() + audiobook.tStart)     && audiobook.status === PsychoJS.Status.STARTED) {
    audiobook.stop();  // stop the sound (if longer than duration)
    audiobook.status = PsychoJS.Status.FINISHED;
  }
  
  // *fixation* updates
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  for (const thisComponent of AudioBookComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  } else {
    return Scheduler.Event.NEXT;
  }
};
}

function AudioBookRoutineEnd(snapshot) {
return async function () {
  //--- Ending Routine 'AudioBook' ---
  for (const thisComponent of AudioBookComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  psychoJS.experiment.addData('AudioBook.stopped', globalClock.getTime());
  audiobook.stop();  // ensure sound has stopped at end of Routine
  // the Routine "AudioBook" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  // Routines running outside a loop should always advance the datafile row
  if (currentLoop === psychoJS.experiment) {
    psychoJS.experiment.nextEntry(snapshot);
  }
  return Scheduler.Event.NEXT;
}
}

function QuestionRoutineBegin(snapshot) {
return async function () {
  TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
  
  //--- Prepare to start Routine 'Question' ---
  t = 0;
  frameN = -1;
  continueRoutine = true; // until we're told otherwise
  QuestionClock.reset();
  routineTimer.reset();
  QuestionMaxDurationReached = false;
  // update component parameters for each repeat
  question.setText(question);
  answer.setText('');
  answer.refresh();
  end_audiobook1.keys = undefined;
  end_audiobook1.rt = undefined;
  _end_audiobook1_allKeys = [];
  psychoJS.experiment.addData('Question.started', globalClock.getTime());
  QuestionMaxDuration = null
  // keep track of which components have finished
  QuestionComponents = [];
  QuestionComponents.push(question);
  QuestionComponents.push(answer);
  QuestionComponents.push(end_audiobook1);
  
  for (const thisComponent of QuestionComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  return Scheduler.Event.NEXT;
}
}

function QuestionRoutineEachFrame() {
return async function () {
  //--- Loop for each frame of Routine 'Question' ---
  // get current time
  t = QuestionClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *question* updates
  if (question.status === PsychoJS.Status.STARTED && Boolean(0)) {
    question.setAutoDraw(false);
  }
  
  
  // *answer* updates
  if (t >= 2.5 && answer.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    answer.tStart = t;  // (not accounting for frame time here)
    answer.frameNStart = frameN;  // exact frame index
    
    answer.setAutoDraw(true);
  }
  
  frameRemains = 2.5 + 60 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
  if (answer.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    answer.setAutoDraw(false);
  }
  
  
  // *end_audiobook1* updates
  if (t >= 8 && end_audiobook1.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    end_audiobook1.tStart = t;  // (not accounting for frame time here)
    end_audiobook1.frameNStart = frameN;  // exact frame index
    
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { end_audiobook1.clock.reset(); });  // t=0 on next screen flip
    psychoJS.window.callOnFlip(function() { end_audiobook1.start(); }); // start on screen flip
    psychoJS.window.callOnFlip(function() { end_audiobook1.clearEvents(); });
  }
  
  if (end_audiobook1.status === PsychoJS.Status.STARTED) {
    let theseKeys = end_audiobook1.getKeys({keyList: ['return'], waitRelease: false});
    _end_audiobook1_allKeys = _end_audiobook1_allKeys.concat(theseKeys);
    if (_end_audiobook1_allKeys.length > 0) {
      end_audiobook1.keys = _end_audiobook1_allKeys[_end_audiobook1_allKeys.length - 1].name;  // just the last key pressed
      end_audiobook1.rt = _end_audiobook1_allKeys[_end_audiobook1_allKeys.length - 1].rt;
      end_audiobook1.duration = _end_audiobook1_allKeys[_end_audiobook1_allKeys.length - 1].duration;
      // a response ends the routine
      continueRoutine = false;
    }
  }
  
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  for (const thisComponent of QuestionComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  } else {
    return Scheduler.Event.NEXT;
  }
};
}

function QuestionRoutineEnd(snapshot) {
return async function () {
  //--- Ending Routine 'Question' ---
  for (const thisComponent of QuestionComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  psychoJS.experiment.addData('Question.stopped', globalClock.getTime());
  psychoJS.experiment.addData('answer.text',answer.text)
  // update the trial handler
  if (currentLoop instanceof MultiStairHandler) {
    currentLoop.addResponse(end_audiobook1.corr, level);
  }
  psychoJS.experiment.addData('end_audiobook1.keys', end_audiobook1.keys);
  if (typeof end_audiobook1.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('end_audiobook1.rt', end_audiobook1.rt);
      psychoJS.experiment.addData('end_audiobook1.duration', end_audiobook1.duration);
      routineTimer.reset();
      }
  
  end_audiobook1.stop();
  // the Routine "Question" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  // Routines running outside a loop should always advance the datafile row
  if (currentLoop === psychoJS.experiment) {
    psychoJS.experiment.nextEntry(snapshot);
  }
  return Scheduler.Event.NEXT;
}
}

function SpacebarContinueRoutineBegin(snapshot) {
return async function () {
  TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
  
  //--- Prepare to start Routine 'SpacebarContinue' ---
  t = 0;
  frameN = -1;
  continueRoutine = true; // until we're told otherwise
  SpacebarContinueClock.reset();
  routineTimer.reset();
  SpacebarContinueMaxDurationReached = false;
  // update component parameters for each repeat
  spacebar_response.keys = undefined;
  spacebar_response.rt = undefined;
  _spacebar_response_allKeys = [];
  psychoJS.experiment.addData('SpacebarContinue.started', globalClock.getTime());
  SpacebarContinueMaxDuration = null
  // keep track of which components have finished
  SpacebarContinueComponents = [];
  SpacebarContinueComponents.push(spacebar_text);
  SpacebarContinueComponents.push(spacebar_response);
  
  for (const thisComponent of SpacebarContinueComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  return Scheduler.Event.NEXT;
}
}

function SpacebarContinueRoutineEachFrame() {
return async function () {
  //--- Loop for each frame of Routine 'SpacebarContinue' ---
  // get current time
  t = SpacebarContinueClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *spacebar_text* updates
  if (t >= 0.25 && spacebar_text.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    spacebar_text.tStart = t;  // (not accounting for frame time here)
    spacebar_text.frameNStart = frameN;  // exact frame index
    
    spacebar_text.setAutoDraw(true);
  }
  
  
  // *spacebar_response* updates
  if (t >= 0.5 && spacebar_response.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    spacebar_response.tStart = t;  // (not accounting for frame time here)
    spacebar_response.frameNStart = frameN;  // exact frame index
    
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { spacebar_response.clock.reset(); });  // t=0 on next screen flip
    psychoJS.window.callOnFlip(function() { spacebar_response.start(); }); // start on screen flip
    psychoJS.window.callOnFlip(function() { spacebar_response.clearEvents(); });
  }
  
  if (spacebar_response.status === PsychoJS.Status.STARTED) {
    let theseKeys = spacebar_response.getKeys({keyList: ['space'], waitRelease: false});
    _spacebar_response_allKeys = _spacebar_response_allKeys.concat(theseKeys);
    if (_spacebar_response_allKeys.length > 0) {
      spacebar_response.keys = _spacebar_response_allKeys[_spacebar_response_allKeys.length - 1].name;  // just the last key pressed
      spacebar_response.rt = _spacebar_response_allKeys[_spacebar_response_allKeys.length - 1].rt;
      spacebar_response.duration = _spacebar_response_allKeys[_spacebar_response_allKeys.length - 1].duration;
      // a response ends the routine
      continueRoutine = false;
    }
  }
  
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  for (const thisComponent of SpacebarContinueComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  } else {
    return Scheduler.Event.NEXT;
  }
};
}

function SpacebarContinueRoutineEnd(snapshot) {
return async function () {
  //--- Ending Routine 'SpacebarContinue' ---
  for (const thisComponent of SpacebarContinueComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  psychoJS.experiment.addData('SpacebarContinue.stopped', globalClock.getTime());
  // update the trial handler
  if (currentLoop instanceof MultiStairHandler) {
    currentLoop.addResponse(spacebar_response.corr, level);
  }
  psychoJS.experiment.addData('spacebar_response.keys', spacebar_response.keys);
  if (typeof spacebar_response.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('spacebar_response.rt', spacebar_response.rt);
      psychoJS.experiment.addData('spacebar_response.duration', spacebar_response.duration);
      routineTimer.reset();
      }
  
  spacebar_response.stop();
  // the Routine "SpacebarContinue" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  // Routines running outside a loop should always advance the datafile row
  if (currentLoop === psychoJS.experiment) {
    psychoJS.experiment.nextEntry(snapshot);
  }
  return Scheduler.Event.NEXT;
}
}

function LastPromptRoutineBegin(snapshot) {
return async function () {
  TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
  
  //--- Prepare to start Routine 'LastPrompt' ---
  t = 0;
  frameN = -1;
  continueRoutine = true; // until we're told otherwise
  LastPromptClock.reset();
  routineTimer.reset();
  LastPromptMaxDurationReached = false;
  // update component parameters for each repeat
  rating_response.setText('');
  rating_response.refresh();
  key_resp.keys = undefined;
  key_resp.rt = undefined;
  _key_resp_allKeys = [];
  psychoJS.experiment.addData('LastPrompt.started', globalClock.getTime());
  LastPromptMaxDuration = null
  // keep track of which components have finished
  LastPromptComponents = [];
  LastPromptComponents.push(last_prompt_text);
  LastPromptComponents.push(rating_response);
  LastPromptComponents.push(key_resp);
  
  for (const thisComponent of LastPromptComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  return Scheduler.Event.NEXT;
}
}

function LastPromptRoutineEachFrame() {
return async function () {
  //--- Loop for each frame of Routine 'LastPrompt' ---
  // get current time
  t = LastPromptClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *last_prompt_text* updates
  if (t >= 0.0 && last_prompt_text.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    last_prompt_text.tStart = t;  // (not accounting for frame time here)
    last_prompt_text.frameNStart = frameN;  // exact frame index
    
    last_prompt_text.setAutoDraw(true);
  }
  
  frameRemains = 0.0 + 120 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
  if (last_prompt_text.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    last_prompt_text.setAutoDraw(false);
  }
  
  
  // *rating_response* updates
  if (t >= 0.0 && rating_response.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    rating_response.tStart = t;  // (not accounting for frame time here)
    rating_response.frameNStart = frameN;  // exact frame index
    
    rating_response.setAutoDraw(true);
  }
  
  frameRemains = 0.0 + 60 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
  if (rating_response.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    rating_response.setAutoDraw(false);
  }
  
  
  // *key_resp* updates
  if (t >= 0.2 && key_resp.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_resp.tStart = t;  // (not accounting for frame time here)
    key_resp.frameNStart = frameN;  // exact frame index
    
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { key_resp.clock.reset(); });  // t=0 on next screen flip
    psychoJS.window.callOnFlip(function() { key_resp.start(); }); // start on screen flip
    psychoJS.window.callOnFlip(function() { key_resp.clearEvents(); });
  }
  
  if (key_resp.status === PsychoJS.Status.STARTED) {
    let theseKeys = key_resp.getKeys({keyList: ['1', '2', '3', '4', '5', 'num_1', 'num_2', 'num_3', 'num_4', 'num_5'], waitRelease: false});
    _key_resp_allKeys = _key_resp_allKeys.concat(theseKeys);
    if (_key_resp_allKeys.length > 0) {
      key_resp.keys = _key_resp_allKeys[_key_resp_allKeys.length - 1].name;  // just the last key pressed
      key_resp.rt = _key_resp_allKeys[_key_resp_allKeys.length - 1].rt;
      key_resp.duration = _key_resp_allKeys[_key_resp_allKeys.length - 1].duration;
      // a response ends the routine
      continueRoutine = false;
    }
  }
  
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  for (const thisComponent of LastPromptComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  } else {
    return Scheduler.Event.NEXT;
  }
};
}

function LastPromptRoutineEnd(snapshot) {
return async function () {
  //--- Ending Routine 'LastPrompt' ---
  for (const thisComponent of LastPromptComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  psychoJS.experiment.addData('LastPrompt.stopped', globalClock.getTime());
  psychoJS.experiment.addData('rating_response.text',rating_response.text)
  // update the trial handler
  if (currentLoop instanceof MultiStairHandler) {
    currentLoop.addResponse(key_resp.corr, level);
  }
  psychoJS.experiment.addData('key_resp.keys', key_resp.keys);
  if (typeof key_resp.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('key_resp.rt', key_resp.rt);
      psychoJS.experiment.addData('key_resp.duration', key_resp.duration);
      routineTimer.reset();
      }
  
  key_resp.stop();
  // the Routine "LastPrompt" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  // Routines running outside a loop should always advance the datafile row
  if (currentLoop === psychoJS.experiment) {
    psychoJS.experiment.nextEntry(snapshot);
  }
  return Scheduler.Event.NEXT;
}
}

function GoodByeRoutineBegin(snapshot) {
return async function () {
  TrialHandler.fromSnapshot(snapshot); // ensure that .thisN vals are up to date
  
  //--- Prepare to start Routine 'GoodBye' ---
  t = 0;
  frameN = -1;
  continueRoutine = true; // until we're told otherwise
  GoodByeClock.reset();
  routineTimer.reset();
  GoodByeMaxDurationReached = false;
  // update component parameters for each repeat
  key_resp_end.keys = undefined;
  key_resp_end.rt = undefined;
  _key_resp_end_allKeys = [];
  psychoJS.experiment.addData('GoodBye.started', globalClock.getTime());
  GoodByeMaxDuration = null
  // keep track of which components have finished
  GoodByeComponents = [];
  GoodByeComponents.push(congrats_text);
  GoodByeComponents.push(press_bar_text);
  GoodByeComponents.push(key_resp_end);
  
  for (const thisComponent of GoodByeComponents)
    if ('status' in thisComponent)
      thisComponent.status = PsychoJS.Status.NOT_STARTED;
  return Scheduler.Event.NEXT;
}
}

function GoodByeRoutineEachFrame() {
return async function () {
  //--- Loop for each frame of Routine 'GoodBye' ---
  // get current time
  t = GoodByeClock.getTime();
  frameN = frameN + 1;// number of completed frames (so 0 is the first frame)
  // update/draw components on each frame
  
  // *congrats_text* updates
  if (t >= 0.0 && congrats_text.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    congrats_text.tStart = t;  // (not accounting for frame time here)
    congrats_text.frameNStart = frameN;  // exact frame index
    
    congrats_text.setAutoDraw(true);
  }
  
  frameRemains = 0.0 + 120 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
  if (congrats_text.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    congrats_text.setAutoDraw(false);
  }
  
  
  // *press_bar_text* updates
  if (t >= 0.25 && press_bar_text.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    press_bar_text.tStart = t;  // (not accounting for frame time here)
    press_bar_text.frameNStart = frameN;  // exact frame index
    
    press_bar_text.setAutoDraw(true);
  }
  
  frameRemains = 0.25 + 150 - psychoJS.window.monitorFramePeriod * 0.75;// most of one frame period left
  if (press_bar_text.status === PsychoJS.Status.STARTED && t >= frameRemains) {
    press_bar_text.setAutoDraw(false);
  }
  
  
  // *key_resp_end* updates
  if (t >= 0.0 && key_resp_end.status === PsychoJS.Status.NOT_STARTED) {
    // keep track of start time/frame for later
    key_resp_end.tStart = t;  // (not accounting for frame time here)
    key_resp_end.frameNStart = frameN;  // exact frame index
    
    // keyboard checking is just starting
    psychoJS.window.callOnFlip(function() { key_resp_end.clock.reset(); });  // t=0 on next screen flip
    psychoJS.window.callOnFlip(function() { key_resp_end.start(); }); // start on screen flip
    psychoJS.window.callOnFlip(function() { key_resp_end.clearEvents(); });
  }
  
  if (key_resp_end.status === PsychoJS.Status.STARTED) {
    let theseKeys = key_resp_end.getKeys({keyList: ['space'], waitRelease: false});
    _key_resp_end_allKeys = _key_resp_end_allKeys.concat(theseKeys);
    if (_key_resp_end_allKeys.length > 0) {
      key_resp_end.keys = _key_resp_end_allKeys[_key_resp_end_allKeys.length - 1].name;  // just the last key pressed
      key_resp_end.rt = _key_resp_end_allKeys[_key_resp_end_allKeys.length - 1].rt;
      key_resp_end.duration = _key_resp_end_allKeys[_key_resp_end_allKeys.length - 1].duration;
      // a response ends the routine
      continueRoutine = false;
    }
  }
  
  // check for quit (typically the Esc key)
  if (psychoJS.experiment.experimentEnded || psychoJS.eventManager.getKeys({keyList:['escape']}).length > 0) {
    return quitPsychoJS('The [Escape] key was pressed. Goodbye!', false);
  }
  
  // check if the Routine should terminate
  if (!continueRoutine) {  // a component has requested a forced-end of Routine
    return Scheduler.Event.NEXT;
  }
  
  continueRoutine = false;  // reverts to True if at least one component still running
  for (const thisComponent of GoodByeComponents)
    if ('status' in thisComponent && thisComponent.status !== PsychoJS.Status.FINISHED) {
      continueRoutine = true;
      break;
    }
  
  // refresh the screen if continuing
  if (continueRoutine) {
    return Scheduler.Event.FLIP_REPEAT;
  } else {
    return Scheduler.Event.NEXT;
  }
};
}

function GoodByeRoutineEnd(snapshot) {
return async function () {
  //--- Ending Routine 'GoodBye' ---
  for (const thisComponent of GoodByeComponents) {
    if (typeof thisComponent.setAutoDraw === 'function') {
      thisComponent.setAutoDraw(false);
    }
  }
  psychoJS.experiment.addData('GoodBye.stopped', globalClock.getTime());
  // update the trial handler
  if (currentLoop instanceof MultiStairHandler) {
    currentLoop.addResponse(key_resp_end.corr, level);
  }
  psychoJS.experiment.addData('key_resp_end.keys', key_resp_end.keys);
  if (typeof key_resp_end.keys !== 'undefined') {  // we had a response
      psychoJS.experiment.addData('key_resp_end.rt', key_resp_end.rt);
      psychoJS.experiment.addData('key_resp_end.duration', key_resp_end.duration);
      routineTimer.reset();
      }
  
  key_resp_end.stop();
  // the Routine "GoodBye" was not non-slip safe, so reset the non-slip timer
  routineTimer.reset();
  
  // Routines running outside a loop should always advance the datafile row
  if (currentLoop === psychoJS.experiment) {
    psychoJS.experiment.nextEntry(snapshot);
  }
  return Scheduler.Event.NEXT;
}
}

function importConditions(currentLoop) {
  return async function () {
    psychoJS.importAttributes(currentLoop.getCurrentTrial());
    return Scheduler.Event.NEXT;
    };
}

async function quitPsychoJS(message, isCompleted) {
// Check for and save orphaned data
if (psychoJS.experiment.isEntryEmpty()) {
  psychoJS.experiment.nextEntry();
}
psychoJS.window.close();
psychoJS.quit({message: message, isCompleted: isCompleted});

return Scheduler.Event.QUIT;
}
