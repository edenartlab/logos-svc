import os
import requests
import tempfile

from .. import utils
from ..plugins import replicate, elevenlabs, s3
from ..character import Character, EdenCharacter
from ..scenarios import story
from ..models import StoryRequest
from .animation import screenplay_clip

MAX_PIXELS = 1024 * 1024
MAX_WORKERS = 3


def animated_story(request: StoryRequest):
    screenplay = story(request)
    #screenplay = {'clips': [{'voiceover': 'narrator', 'character': None, 'speech': 'In a quaint ski town replete with snowy peaks and the charm of winter, there lies a forgotten legend eager to reclaim his throne.', 'image_description': 'The sun glints off the snow-capped mountains, as a quaint alpine village stirs to life in the valley below.'}, {'voiceover': 'character', 'character': 'Viper', 'speech': "You see this medal? That's the mark of a champion. Sometimes I miss the cheers, the rush of the wind... the taste of victory.", 'image_description': 'A bronze-hued man, Viper, sits in a cozy ski lodge. Various medals and trophies litter the space around him. His eyes gleam with pride, yet carry a tinge of yearning.'}, {'voiceover': 'narrator', 'character': None, 'speech': 'But life, like the serpentine trails he once conquered, took an unexpected turn when a new star shot across his sky.', 'image_description': 'Laughter echoes through the local gym as a towering woman playfully scores basket after basket on an indoor court.'}, {'voiceover': 'character', 'character': 'Linda', 'speech': "I thought I knew what it was to be at the top, but Linda, she... she's a mountain of her own, you know?", 'image_description': "Viper gazes through the gym's glass doors, admiration painted on his features as he watches a nine-foot-tall woman, Linda, effortlessly dominate the basketball court."}, {'voiceover': 'narrator', 'character': None, 'speech': 'From the frozen slopes to the polished hardwood, it was as if fate had crafted a match not even the sports gods could have predicted.', 'image_description': 'A cosmic dance of stars and snowflakes swirls around the figures of Viper and Linda as they first meet, their differences dwarfed by the evident spark between them.'}, {'voiceover': 'character', 'character': 'Viper', 'speech': "Hey Linda, want to trade some stories? I've got a lifetime on the slopes and you've got... well, a view from the top. Literally.", 'image_description': 'Viper approaches Linda with a mischievous smirk, leaning on a basketball. Linda towers above him, her presence as commanding as her height.'}, {'voiceover': 'character', 'character': 'Linda', 'speech': "I am Linda I am so cool", 'image_description': 'Linda plays basketball at night'}]}
    print(screenplay)
    
    characters = {
        character_id: EdenCharacter(character_id) 
        for character_id in request.character_ids + [request.narrator_id]
    }

    character_name_lookup = {
        character.name: character_id
        for character_id, character in characters.items()
    }

    print("LETS MAKE ALL THE CHARACTERS")
    print("LETS MAKE ALL THE CHARACTERS 2")
    thechars = [clip['character'] for clip in screenplay['clips']]
    print("LETS MAKE ALL THE CHARACTERS 3")
    print(thechars)
    print(character_name_lookup)
    # if any character is new, assign a random voice
    for clip in screenplay['clips']:
        print(" --> ", clip['character'], clip['voiceover'])
        if clip['character']:
            character_name = clip['character']
            print("ceck " , character_name)
            print("ceck2 " , character_name)
            print("look here", character_name_lookup)
            print("look there", characters)
            if character_name not in character_name_lookup:
                print("MAKE A NEW CHARACTER", character_name)
                characters[character_name] = Character(name=character_name)
                character_name_lookup[character_name] = character_name
            else:
                print("CHARACTER IS FOUND", character_name)
            print("check on voice...", character_name)
            print("about to chekc ovice")
            print("is it voice? 0")
            print(characters)
            character_id = character_name_lookup[character_name]
            print("got id", character_id)
            print(characters[character_id])
            print("ok 3")
            #print(characters[character_name])
            print("ok 4")
            print("is it voice?", characters[character_id].voice)
            if not characters[character_id].voice:
                print("NO VOICE, GET A RANDOM VOICE")
                voice_id = elevenlabs.get_random_voice()
                characters[character_id].voice = voice_id
            print("is it voice now?", characters[character_id].voice)
        print("------")    
        
    print("THIS IS THE END!")
                 
    


    # width, height = utils.calculate_target_dimensions(images, MAX_PIXELS)
    width, height = 1792, 1024

    def run_story_segment(clip, idx):
        if clip['voiceover'] == 'character':
            character_id = character_name_lookup[clip['character']]
            # character_id = characters[clip['character']]
            character = characters.get(character_id)
        else:
            character = characters[request.narrator_id]
        #print("")
        output_filename, thumbnail_url = screenplay_clip(
            character,
            clip['speech'],
            clip['image_description'],
            width,
            height
        )
        return output_filename, thumbnail_url

    results = utils.process_in_parallel(
        screenplay['clips'], 
        run_story_segment,
        max_workers=MAX_WORKERS
    )

    video_files = [video_file for video_file, thumbnail in results]
    thumbnail_url = results[0][1]

    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_output_file:
        utils.concatenate_videos(video_files, temp_output_file.name)
        with open(temp_output_file.name, 'rb') as f:
            video_bytes = f.read()
        output_url = s3.upload(video_bytes, "mp4")

    # clean up clips
    for video_file in video_files:
        os.remove(video_file)

    return output_url, thumbnail_url
