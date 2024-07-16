var timer1 = document.getElementById('timer1');
var timer2 = document.getElementById('timer2');
var timer3 = document.getElementById('timer3');
var startAll = document.getElementById('startAll');

window.onload = function(){
  stopwatch('Timer1');
  stopwatch('Timer2');
  stopwatch('Timer3');
}

function stopwatch(element){
  let [milliseconds,seconds,minutes] = [0,0,0];
  let timerRef = document.querySelector('.timerDisplay' + element);
  let int = null;
  let elapsed = 0;
  let beforePause = 0;
  let start = 0;
  let started = false;
  
  document.getElementById('startTimer' + element).addEventListener('click', ()=>{
      if(int!==null){
          clearInterval(int);
      }
      if (started == false) {
        started = true;
        start = Date.now();
      }
      int = setInterval(displayTimer, 10);
  });

  document.getElementById('startAll').addEventListener('click', ()=>{
      if(int!==null){
          clearInterval(int);
      }
      if (started == false) {
        started = true;
        start = Date.now();
      }
      int = setInterval(displayTimer,10);
  });

  document.getElementById('resetAll').addEventListener('click', ()=>{
      elapsed = 0;
      started = false;
      beforePause = 0;
      document.getElementById('millis' + element).value = '';
      clearInterval(int);
      [milliseconds,seconds,minutes] = [0,0,0];
      timerRef.innerHTML = '00 : 00 : 000';
  });
    
  document.getElementById('pauseTimer' + element).addEventListener('click', ()=>{
    if (started == true){
      elapsed = beforePause + Math.abs(start - Date.now())
      started = false;
      beforePause = elapsed;
      document.getElementById('millis' + element).value = elapsed/1000;
      clearInterval(int);
    }  
  });
  
  document.getElementById('resetTimer' + element).addEventListener('click', ()=>{
      elapsed = 0;
      started = false;
      beforePause = 0;
      document.getElementById('millis' + element).value = '';
      clearInterval(int);
      [milliseconds,seconds,minutes] = [0,0,0];
      timerRef.innerHTML = '00 : 00 : 000';
  });
  
  function displayTimer(){
    elapsed = beforePause + Math.abs(start - Date.now());
    milliseconds = elapsed % 1000;
    seconds = Math.floor(elapsed/1000) % 60;
    minutes = Math.floor(elapsed/60000);
  
   let m = minutes < 10 ? "0" + minutes : minutes;
   let s = seconds < 10 ? "0" + seconds : seconds;
   let ms = milliseconds < 10 ? "00" + milliseconds : milliseconds < 100 ? "0" + milliseconds : milliseconds;
  
   timerRef.innerHTML = `${m} : ${s} : ${ms}`;
  }                                              
}