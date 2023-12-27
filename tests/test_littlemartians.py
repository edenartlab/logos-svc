import random
from logos.scenarios import comic_book
from logos.sample_data.characters.littlemartians import verdelis, hypatia

def test_comic_book_function():
    """
    Test if the dialogue function returns a conversation
    """
    
    setting = random.choice([
        "physical reality", 
        "human imaginarium"
    ])
    
    synopsis = random.choice([
        "You meet an alien",
        "You meet a robot",
        "You're hungry",
        "The world's blowing up",
        "You found a genie in the lamp",
        "You're in a desert",
        "You're trying to remember a long-forgotten memory",
        "what should i do tonight?",
        "does this dress make me look good?",
        "Hello",
        "cknsv,mfds3"
    ])

    num_scenes = random.choice([3, 4])

    comic = comic_book(verdelis, setting, synopsis, num_scenes, model="gpt-4-1106-preview")
    
    print(comic)

    # assert type(comic) == list
    # assert len(comic) > 0

test_comic_book_function()