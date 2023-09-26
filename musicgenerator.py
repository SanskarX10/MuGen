

import tensorflow.keras as keras
import json
import numpy as np
import music21 as m21
from preprocess import SEQUENCE_LENGTH, MAPPING_PATH

class MelodyGenerator:

    def __init__(self, model_path = "model.h5"):
        self.model_path = model_path
        self.model = keras.models.load_model(model_path)

        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)

        self._start_symbols = ["/"] * SEQUENCE_LENGTH


    def generate_melody(self, seed, num_steps, max_Sequence_length, temperature):
        # temprature = {0,1}

        #create seed with start
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed

        # map seed to integer
        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            #limit the seed to max seq len
            seed = seed[-max_Sequence_length:]

            #one hot encode
            onehot_seed = keras.utils.to_categorical(seed, num_classes=len(self._mappings))
            # (1, max_Seq_len , num_of_symbol in vocab) to meet keras method requirement
            onehot_seed = onehot_seed[np.newaxis, ...] # 2d -> 3d

            #make a prediction
            probabilities = self.model.predict(onehot_seed)[0]

            #[0.1, 0.2, 0.1, 0.4]
            output_int = self._sample_with_temprature(probabilities, temperature)

            #update_Seed
            seed.append(output_int)

            #map int to our encoding
            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]

            #check wheather we are at the end of the melody
            if output_symbol == "/":
                break

            #update if not true
            melody.append(output_symbol)

        return melody




    def _sample_with_temprature(self, probabilities, temperature):
        #temprature -> infinite
        #temprature -> 0
        #temprature = 1
        predictions = np.log(probabilities) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilities))
        index = np.random.choice(choices, p = probabilities)

        return index

    def save_melody(self, melody, step_duration = 0.25, format = "midi", file_name="mel.midi"):

        #create a music21 stream
        stream = m21.stream.Stream()


        #parse all the symbols and create notes and rest
        #60 ___ r_62__
        start_symbol = None
        step_counter = 1

        for i,symbol in enumerate(melody):

            #case in which we have a note/rest
            if symbol != "_" or i + 1 == len(melody):
                # to make sure we are dealing with note / beyond pehla wala
                if start_symbol is not None:
                    quarter_length_duration = step_duration * step_counter

                    #handle rest
                    if start_symbol == "r":
                        m21_event = m21.note.Rest(quarterLength = quarter_length_duration)

                    #handle note
                    else:
                        m21_event =m21.note.Note(int(start_symbol), quarterLength = quarter_length_duration)

                    stream.append(m21_event)

                    #reset the step counter
                    step_counter = 1

                start_symbol = symbol

            #case in which we have a holding sign
            else:
                step_counter += 1




        #write the m21 stream to midi file
        stream.write(format, file_name)


if __name__ == "__main__":
    mg = MelodyGenerator()
    seed = "69 _ 72 _ _ _ 74 _ _ _ 76 _ _ _ _ "
    melody = mg.generate_melody(seed, 500, SEQUENCE_LENGTH, 0.7)
    print(melody)
    mg.save_melody(melody)







