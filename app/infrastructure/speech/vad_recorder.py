import wave

import numpy as np
import sounddevice as sd
import webrtcvad

from app.core.logger import logger


class VADRecorder:
    @staticmethod
    def record(
        output_path: str = "temp_audio/input.wav",
    ) -> str:
        sample_rate = 16000
        frame_duration = 30
        frame_size = int(sample_rate * frame_duration / 1000)

        vad = webrtcvad.Vad(2)

        logger.info("Listening...")

        recording = []
        silence_frames = 0
        speech_detected = False

        silence_limit = 25

        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
            blocksize=frame_size,
        ) as stream:

            while True:
                audio_chunk, _ = stream.read(frame_size)

                audio_bytes = audio_chunk.tobytes()

                is_speech = vad.is_speech(
                    audio_bytes,
                    sample_rate,
                )

                if is_speech:
                    speech_detected = True
                    silence_frames = 0

                    recording.append(audio_chunk.copy())

                else:
                    if speech_detected:
                        silence_frames += 1

                        recording.append(audio_chunk.copy())

                if speech_detected and silence_frames > silence_limit:
                    break

        logger.info("Speech finished.")

        audio_data = np.concatenate(
            recording,
            axis=0,
        )

        with wave.open(
            output_path,
            "wb",
        ) as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)

            wf.writeframes(
                audio_data.tobytes(),
            )

        return output_path
