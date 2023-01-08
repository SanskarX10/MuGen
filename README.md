# MuGen
Artificial Melody Generator using RNN-LSTMS


Mu-Gen ( Artificial music generator ) :

OVER VIEW :
    tools :
    keras / tensorflow: to program the model 
    Music 21: to process symbolic music data
    Muse score: convert notations to music

    What a Melody is ?
    > sequence of notes and rests
    > y axis : pitch
    > x axis : time

    Melody Generation Task :
    > treat melody as time series (time series have samples that are taken at evenly spaced position in time )
    > time series prediction
    > vocabulary of nodes

    Give a chunk of nodes , train and predict next melody , what we are doing is give , get , append , repeat

    Why RNNs ?
    > melodies have long patterns
    > lstm finishes depleting gradients

    Data :
    > folk melodies , cause they are simple
    > we are using esac dataset

MUSICAL INTIUTION :
    Note = pitch + duration

    PITCH -
    pitch : how high or low the node is
    two nodes can be same but can have different frequency
    that's why we have note name + octave , eg - C3,D4
    chroma(sound) is same but octave is different (12 octaves are there)
    we will use MIDI format
        # midi maps notes names to numbers for manipulation by computers

    DURATION -
    'duration' can be represented by note values :
        # 1 whole note = 4 beats
        # 1 half note = 2 beats
        # 1 quarter note = 1 beat
        # 1 eighth note = 1/2 a beat
        # 1 sixteenth note = 1/4 beat

        'time duration' :
            represented by time signature ( n/d ) :
            n / d =
                > n = number of beats in a bar / portion
                > d = type of note which is equal to 1 beat
        melodies are shaped by time signature
        our network needs to learn time signature

    KEY -
    group of pitches that forms centre of the piece
    tonic + mode
    eg - C major , D minor

        Tonic note :
        > pitch that provides the sense of arrival
        > harmonic centre of gravity
        > found at the beginning and end , feels like a rest to the music

        Mode ( Major/ Minor ) :
        > joyous music is  major , uppercase letters
        > sad is minor , lowercase letters

     12 notes x 2 modes =  24 keys
     networks should be able to learn where to rest , tense moments , how to arrange

DATA PREPROCESSING :

    TRANSPOSITION :
    reduction of 24 keys to 2 keys
    we will shift everything to c major and a minor
        > moving collection of notes up or down by a given interval
        > change key
        > content remains the same

    MUSIC REPRESENTATION :
    can't use sheet notation
    > time series
    > sample melody at each 16th note
    > each step = 16th node
    > log midi when note occur
    > use _ symbol to hold note
    > "r" for rest

        example -
        : 4/4 time signature - 4 beats in out set , and 4 notes make 1 beat which is equal to 16 samples per bar
        : 4 samples per quarter note

    > time series
    > map time series to integers
    > one hot encoding


    M21 :
    Score -
        parts : a part contains multiple bars (time signature , bass etc ) , can be easily manipulated
        score + parts + measure + notes
       
![Outline](https://github.com/SanskarX10/MuGen/blob/main/image.png?raw=true)
