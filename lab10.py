import json
import pyttsx3, vosk, pyaudio, requests, time

class Recognize:
    def __init__(self):
        model = vosk.Model('model_small')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()
        self.tts = pyttsx3.init()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)
    
        self.commands = {
                "факт": self.get_info,
                "прочитать": self.read_last_fact,
                "убрать": self.delete_last_fact,
                "записать": self.write_last_fact
            }
            
            
        self.fact_history = []

    def speak(self, text):
        self.tts.setProperty("voice", 0)
        self.tts.setProperty("rate", 100)
        self.tts.say(text)
        self.tts.runAndWait()

    def get_info(self):
        url = "http://numbersapi.com/random/math"
        response = requests.get(url)
        self.fact = response.text
        return response.text
    
    def write_last_fact(self):
        self.fact_history.append(self.fact)
        return 'Факт записан'
    
    def read_last_fact(self):
        if self.fact_history != []:
            self.speak(self.fact_history[-1])
            return self.fact_history[-1]
        else:
            return 'Нет фактов для прочтения'

    def delete_last_fact(self):
        if not self.fact_history:
            return "История фактов уже пуста."
        self.fact_history.pop()
        return "Последний факт удалён."

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data):
                result = json.loads(self.record.Result())
                command = result.get("text", "").lower()
                
                if command in self.commands:
                    action = self.commands[command]
                    response = action()
                    print(response)
                elif command:
                    print(f"Неизвестная команда: {command}")



rec = Recognize()
text_gen = rec.listen()
time.sleep(0.5)
rec.stream.start_stream()


