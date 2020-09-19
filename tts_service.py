import azure.cognitiveservices.speech as speechsdk

speech_key, service_region = "fc813bde2c194491b528da6cd361354e", "uksouth"


class TTSService:
    def speech_synthesis_to_wave_file():
        """performs speech synthesis to a wave file"""
        # Creates an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Creates a speech synthesizer using file as audio output.
        # Replace with your own audio file name.
        file_name = "outputaudio.wav"
        file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

        # Receives a text from console input and synthesizes it to wave file.
        while True:
            print("Enter some text that you want to synthesize, Ctrl-Z to exit")
            try:
                text = input()
            except EOFError:
                break
            result = speech_synthesizer.speak_text_async(text).get()
            # Check result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech synthesis canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
