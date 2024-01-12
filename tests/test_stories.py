from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)


prompts = [
    'The four protagonists wake up suddenly, inside of a cube-shaped chamber with 6 hatches on each wall. They have no memory of how they got there, and no idea how to escape.',
    'You are all rap battling each other',
    'you are all having just an insane screaming contes. use lots of ALL CAPS and exclamation points!!!!',
    'You are debating esoteria of art history',
    'Debate the meaning of The Glass Bead Game',
    'aliens are coming to earth and you are all trying to convince them to spare humanity',
]

prompts = [
    # "The group finds themselves in a vast, ancient library with endless rows of books. They must decipher cryptic clues hidden in the tomes to find a way out. The narrator begins the first clip",
    # "You are in a fierce dance-off competition, each showcasing your unique styles and skills in an abandoned warehouse.",
    # "Engage in an over-the-top, theatrical debate as rival chefs in a cooking show, each defending your eccentric and unconventional recipes.",
    # "Discuss the intricacies and philosophical implications of surrealism in modern art.",
    # "Debate the significance and impact of 'Invisible Cities' by Italo Calvino on contemporary literature.",
    # "You're a group of diplomats from Earth negotiating with a council of intergalactic beings, presenting the cultural and scientific achievements of humanity as reasons for Earth's preservation."
    "Embark on a time-traveling adventure to historical landmarks, where each of you must solve a mystery specific to that era and place using only the knowledge and tools available at the time.",

    "Imagine you are contestants in a futuristic game show where challenges involve solving complex puzzles using advanced technology and artificial intelligence.",

    "You're a team of archaeologists uncovering an ancient civilization on Mars, piecing together the history and culture of this Martian society from artifacts and ruins.",

    "Engage in a mock trial set in a fantasy world, where mythical creatures are defending their rights and coexistence with humans.",

    "Discuss the ethical and societal implications of a world where human emotions can be artificially stimulated and controlled through technology.",

    "Debate the potential and risks of creating a utopian society, considering aspects like technology, governance, and human nature.",

    "You are members of an elite space exploration team, encountering and interpreting alien forms of art and communication.",

    "In a world where dreams and reality are indistinguishable, discuss how this affects human perception, creativity, and mental health.",

    "Act as rival inventors at a world fair, each presenting a groundbreaking invention that could change the course of human history.",

    "Engage in a philosophical discussion about the nature of consciousness in a world where artificial intelligence has achieved self-awareness."
]

def test_cinema():
    """
    Test cinema story prompt
    """

    for prompt in prompts:
        request = {
            "character_ids": ["6596129023f1c4b471dbb94a", "6598e117dd06d165264f2277", "6598e103dd06d165264f2247", "6598ee16dd06d16526503ce7"],
            "prompt": prompt
        }

        try:
            response = client.post("/story/cinema", json=request)
            print(response.json())
        except Exception as e:
            print(e)
            continue

    assert response.status_code == 200


# def test_comic():
#     """
#     Test comic book story prompt
#     """
#     request = {
#         "prompt": "Make a comic book."
#     }

#     response = client.post("/story/comic", json=request)
#     print(response.json())

#     assert response.status_code == 200
