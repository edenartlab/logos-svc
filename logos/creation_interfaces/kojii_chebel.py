import random
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from ..plugins import replicate


class Number(Enum):
    one = "one"
    many = "many"


class AspectRatio(Enum):
    portrait = "portrait"
    landscape = "landscape"


class ColorType(Enum):
    color = "color"
    black_and_white = "black and white"


class KojiiChebelRequest(BaseModel):
    """
    A request for Chebel Kojii endpoint
    """

    number: Number
    aspect_ratio: AspectRatio
    abstract: float
    color: ColorType
    seed: Optional[int] = Field(default=None, description="Random seed")


def kojii_chebel(request: KojiiChebelRequest, callback=None):
    lora_scale = 0.44 + 0.52 * request.abstract
    seed = request.seed if request.seed else random.randint(0, 1000000)

    if request.color == ColorType.color:
        prompt = "oil painting, soft pastel colors, skin tones, woman, dance, expressive brushstrokes"
        negative_prompt = "colorful, yellow, blue, watermark, text, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft"
    else:
        prompt = "oil painting, black and white, woman, dance, expressive brushstrokes, charcoal drawing"
        negative_prompt = "color, colors, red, pink, purple, green, orange, yellow, blue,  colorful, watermark, text, tiling, out of frame, blurry, blurred, grainy, signature, cut off, draft"

    # Hardcoded to 1024x1024 as per Chebel's request (aspect ratio of init_img will still get adopted)
    w, h = 1024, 1024

    control_image = random.choice(
        control_images[request.number.value][request.aspect_ratio.value],
    )

    control_image_strength = 0.84
    guidance_scale = 8

    config = {
        "mode": "controlnet",
        "controlnet_type": "canny-edge",
        "text_input": prompt,
        "uc_text": negative_prompt,
        "lora": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/d93ba7c3b642816c3ab2f5c1755539e222e902d52c6a63064feb57a6cd2c5ba7.tar",
        "lora_scale": lora_scale,
        "control_image": f"https://d14i3advvh2bvd.cloudfront.net/{control_image}",
        "control_image_strength": control_image_strength,
        "width": w,
        "height": h,
        "adopt_aspect_from_init_img": True,
        "guidance_scale": guidance_scale,
        "sampler": "euler",
        "steps": 50,
        "seed": seed,
    }

    print("THE CONFIG")
    print(config)

    image_url, thumbnail_url = replicate.sdxl(config)

    return image_url, thumbnail_url


control_images = {
    "one": {
        "landscape": [
            "8ebda1a515ae0039ebda48e5a0ec63760a2e93ad73400ca53b35410e62e6963c.jpg",
            "8032a81fcc90461573956bc7e8f508db3e01acb2b08ac9a76ee104a855ac9069.jpg",
            "f518f97f37e09e8c0416a4854d477f269a8509e87215a154fd680ebf0110a996.jpg",
            "1c1db0caf6820912d87c1aa708b6175c3f067d5a2790c59ceb4a8d653d3aa7c3.jpg",
            "4122db4ac41a19aa78fa87fcaca042a333145491926dba8518e6c9a3ecf6e494.jpg",
            "9b71a786b1b95e57c8fbcb42b1f47924cdd6f79841eec94e03d895e73438203b.jpg",
            "0f013e6854f29c1cacc99b3499bf0bc0d6791e37d43c7d248263beaf63138520.jpg",
            "abc60aea84a8c42ccea090d8f07e3b8ace9de4ed326426fe33b1952ff3f07e8b.jpg",
            "2c4a9ddbacd10a79a9bcf625603d8d5def433ae03372bf46f63acf490f368242.jpg",
            "1fab28fac61b6b600408132ec2fa0f72225edb4fd1364f14bfe77ee3919dcfcf.jpg",
            "368ba85fc478a68e27437ffd415d3b0d8dfd112bad75df4fb9dd3bdf34cacadb.jpg",
            "e49d9dfd3061845d1bd8dfed15680171bb9c69739d0ddffbe177ea6285397ea2.jpg",
            "f51cfa69cf0d6de9ca9caf0339eb869da40ae98a157f3c9beb18073d6fccaa76.jpg",
            "d7a69671264222d63be032ae90f8f5d7cce9cf69be4de6e6179f0009a9bf7cf5.jpg",
            "59c25587126aa00f2af048ceabb721b02e2333272b63e93f469b4d12744faf59.jpg",
            "2b5b2af235e5801a258fe8dbf12caf8049630ca09b4a9b5cde634fabf90d72ed.jpg",
            "13c8d099c40fc4b7684d2c3b0a6a509981ca7df7c38a9137678504dd699e2185.jpg",
            "daa581b6d128ea6ea0d53474e6bddce020b057060d4e9b1a7dd167f62ed0bd21.jpg",
            "d9b85b548f8efe1520eb9f18af5874178c916ceb27e16d7a35c18b6f989dca83.jpg",
            "1e8af71182a57d3fc57cadcc7dfe3fe50e8c838c52413c1bf25793a034858f68.jpg",
            "a451d01e9b62e0a7e7941aeb3fe564c4b9db349e6608647429ac0153de97f601.jpg",
            "6ece5779dae67701393bbfc0bf3c6df4bec371e57107a6a25904291d2fe225e0.jpg",
            "c1088be9c7ba79bb3bc0e503bd4bf69e1eed104b722d79894348ef568aeeda3e.jpg",
            "e0ef02f6968f8598f895c89d785842e67e25333255dd7f0cfc490c4edc6eab9d.jpg",
            "0b6aec5468c4d34caafc39e18db2613e64ace49873ba47888a7a3362899fd151.jpg",
            "aa0a975dc967606d237b875870dc4c7b29c2817f26dc45183bba1d76ec037d8c.jpg",
            "b03123188e9f551ebf6a3a0e612d29b95d8a4e7c5b34ea994ec14bb344787676.jpg",
            "0c7c272ed9bfa13537ee6e6a8f1205a192ceb22e145da3ce3033c622bf6f7ee6.jpg",
            "3598c063456a218f9814e0a57ba330af208a632e66ff26edca2113751109750c.jpg",
            "b97df2a08376819fa493faef585ce2508c07ce62db4894a30fadb57000bb048b.jpg",
            "10d2e4f31e07358672ab765ecbd348e0bd178ea4b986d351e961c05c8d13b468.jpg",
            "c27df729c2d84d6503618d5d8829bc5730e20c4fb6b4eb10f95184e523dd7e70.jpg",
            "be2ae6453793e40a194bbb28cec79858479d0798abf5068cbe61c06480e28dc2.jpg",
            "e79179cea1ada0adb646fb4e4599c9ea890457d95a16977444efa771b67448d7.jpg",
            "7876ed0be2dcf83dfe22dde2ff8cc97130f13b7b2cd6c463ef7650d832358105.jpg",
            "d001ab831408b56ae8d586a8337e6a82824d27b2ec821690297dd87161c51c13.jpg",
            "8b1a62e80d7b70bff6a1351e57dda94acc60d9af795dba5413c0239d0d71cb30.jpg",
            "d415d403f41f49ff4bef261281f2cdd86ceb3998bd75a2e3d98011f8f75b83b2.jpg",
            "6abf1e377adc5a1dfd6c0222605860fdb7a40d5f6c8a0181d0231892c031a0b8.jpg",
            "e6cdcc0d749b1784a128a9de11fd1529fe79715a32f9a4d14e58a88a27a709e7.jpg",
        ],
        "portrait": [
            "1480cea81266c6a270ef572d488ad4b3c90f095998a9ee821279f328015b18e9.jpg",
            "cc4f9e5d32ee9625bdb383655c70c100f9b00e3f93fe566e378645d823f687f3.jpg",
            "a098e815b79a8fc65059853e915333f23e64a581869502a30964b415c8a4e393.jpg",
            "edba6662c687a7c7019a43363038228c4b3d42297c63310a6a8eb25f06c9937f.jpg",
            "4e37422b9a967e380de97bcf1ade0b88616d87d7b0838c127239f44569bd45b5.jpg",
            "b6cca07713f2e65a86f84900a9ddf115d24a671de0039b93534352a44236f5a8.jpg",
            "9222678ca08ea9ccdc7de535f9504e06e993063cd700e6038e820fc008403602.jpg",
            "b32da129363e6c0751176eb05eb0217bd646be459cfec8c28c3a86a10ad845eb.jpg",
            "3dd6084121845ab5513a59e6f9f9903bb8a2f0bafb26ef97292b6f8ab758bee5.jpg",
            "418b3eca95f8d253d4b3a0cd170b7e7accea784e34c8b71fb564c6be7e36aeb3.jpg",
            "0936914da0e5a12b1b94441ab5c8c524afe35abd05c876780e944edf91de8f2a.jpg",
            "768d95806f8086f99dec3c20b945df5e9a7c2c09dd8d5cd4571b9685859da649.jpg",
            "e6ea233b6061ae4d25c46fd69f982700d7ae482a25e556dee443bd86c52f38fa.jpg",
            "5db70b232421a75bac084c9f584b10a8434bb3ec296dd9988d462cce4e17ccb0.jpg",
            "5a836151b3cf2b67673de922f94cb5fa9758d3c954b16d4b29488b1ac16a5170.jpg",
            "39600cbeda67ca2bbe2f188f80c4796a955d4fcd756b880d1df30dd018c4e304.jpg",
            "86c4e1d918e9747919a56e2286651c6aebc10107eddbd364418bdb565a0f87ca.jpg",
            "082ab5993e092e58116d556b1fc9a307b310d0aef3580a4e17969371f48f8cd5.jpg",
            "1a1f80ecb65a023bef6690f327597d6592dc32ee890d010ecb2537acddccb9a1.jpg",
            "1518895075bead9315a53171384a169cbb885e2fa52cb1742c025c8535ae1a7a.jpg",
            "58f46ef2e25d72f85947a5752993b2c546d16b71050f6ed96ed28d5cbeb9f3da.jpg",
            "3757c58a05e3b2f3ead486713e4c621ebc2f57214da33ab2e7efdf3b143bb0b8.jpg",
            "06317a61e49732e23b6adad4a02eaf79e6a3a70da64b302498530c8ca2c5317b.jpg",
            "cc51fbfae08fb08b4f67a2a8c401ba4b2236354ed1a96d5b61be74b15bfbb9c5.jpg",
            "eb8c0d0ee94fce7f18601a275f390e16f265a057a385d810704bb0e71b88a01b.jpg",
            "5b19e15f69bf16ddd37e304c7abf644a4417fb25baa9e68cf77af4ea0af9bea3.jpg",
            "b78def595f3d9c5bbb77f5ed5d7c100b1a5f665549cb14751c46e27492de4749.jpg",
            "fc04af0b215e5ea86f546ba5129ac19a988a9a267616878a4e6805a64e99d31e.jpg",
            "4964ebd71273cffe38313416153333fecb8979c562d1c231dccd69c713a65a80.jpg",
            "290abbf3a188c77941704f9c1ae5323c2faaad10133e2888e0b3ea6bf9b53e62.jpg",
            "bc34256a282af1f038d089021fb49ee938891169b0f23a6dce742366d07724b3.jpg",
            "361aaafd13756f1584cfed4ac74d5f292ac2725f742f943c93d5de378dc1c232.jpg",
            "d623b3eca2bf3b383f043f75882a3ed3b2cc868fe8d01ff7994f6c9fc0a8f484.jpg",
            "ca3c242c2b42b322032e9c0d25f37adc2645e627590650ae151fde44c9f30eac.jpg",
            "d734760e22cfe62357b65ca126b0d6ef36cfb54be82ee7b15bb941720b4ccc39.jpg",
            "5855cdd6100ffafae6680b7b33e493947c4a8946442891b3683dd068b3ca56e6.jpg",
            "f3a81059af28d5f5f33c299cf570fe00227bb2a8620d9c8810ce817abd74e759.jpg",
            "069928e80eebdda3b3585b0cd08dff34fbd63156402f9a78f3c563e350d3fba5.jpg",
            "a4c804802da3fc3a37c24de4dc0c05f2f0b6dd14cd3925f936274d84b91e3916.jpg",
        ],
    },
    "many": {
        "landscape": [
            "4132b39942028d0dd61c890d0cbfb1b369e536a4a9a5a0ad5b352e728ad7f60a.jpg",
            "34ba95f8455263782646e459787091edf8ad99bfbfa2977456d77c85f5b84983.jpg",
            "716f005c1d0882c326902981dd3550af454b36ec50429107cee917f1faef157c.jpg",
            "aad42bdca9f9ad7f627199bb2851c02730493a9fb6513955c0316862a11442fe.jpg",
            "26946b9781557607481b80a69e5dabd9f499866b3526a04d235feec7a9993f1f.jpg",
            "15d1690ba1889679d5582fccd911e9aa50228e46bbffe32a8e31aafe4a5615a6.jpg",
            "fc09015eba913c827fb6cf1c54e3a19ba16a3272d101baa134216fd4cf048b05.jpg",
            "872db3eea11b23b4ac9846ba4118a0673887383bec35ebd2ec9a10ab5c0f7974.jpg",
            "3da4683d548c85d8703e40c8655561bc6bec7d3ab2f013849b8ef7abfb77763e.jpg",
            "1181440ce4dcc1a144198c99ed7e67e30c5a9ea1877da2714df7129025e00d91.jpg",
            "2e2658853df2842826607d3d802cece7a3ca366b21dc4322ecdf7276613e3ac5.jpg",
            "980bac9914a8b9ef7c795c556a50c15ebd83792cb1384d952f01b5fa65300f13.jpg",
            "7c82b5b82c2ca64439676e7ca36fc0786db0244644f9001949f4f04f4b2f6ba7.jpg",
            "79fc95d169c6e47b6fcf32ff6e244dfa1190314788f5de0023929164f09aca31.jpg",
            "f4beb9e335c8396ea34ad8f647d35b2437cd288439007bff0409379a4cae8693.jpg",
            "bd8b871bb18844bfe358dad05384e4bc33a9cf9b5dc765def9648e5553bc949f.jpg",
            "f5977edfd87dfc2ff30b955a3491d6e9604d616a62ef8659a53f01d9011ad098.jpg",
            "1d6b08ffd2df14bf80f6244b67dabfa211b06d8c9fc53c882209da45e1bbc685.jpg",
            "7ee81900859061c0df19cad28a416aa768840694bf19f57d2c662a00ba16f928.jpg",
            "2d881252265382639dcdee9fdf09bf93893c094b4ea0af16aa43b984eaf0f35d.jpg",
            "65305372dfb343f06e86c0c055d98a2420bc00323b2486347c7509c7393ae09f.jpg",
            "ea06adc8ef98bb94754df0d2ca074a3b56a006bb8e3df2ba42d2714d147852a2.jpg",
            "61d876c6bf666d24dae1be50463674bb71d6a56522ae7160ca11e04f082c2385.jpg",
            "69ccb96ecc15ea3baf74e1e98c172da8ce7ff67b949160242a700cd9b4fa3bee.jpg",
            "58494c985f330352b74a67b3015e12ccfc0c7b9417bb5b566e86106469a88e70.jpg",
            "2863b52dfcd7f49a93db4752aa77abb7452b27344bc770c6db78ecbaef66c4df.jpg",
            "19de0fe7666805efd7c2d54a08df6947fb35a3c0ceab4daa40ba9073718c4c85.jpg",
            "af5ca413bd32ca1caed5e493eba1d0baf97d58c5010390fbb02a013bc8a812fb.jpg",
            "ae0fa5f4fa07970dc701e74078a5292527789494c66d452e7b6a06597805d933.jpg",
            "58413cd6acd2d340ee3536a67aafd7f55809c109d9784f346bf0826574bd0dcd.jpg",
            "2f94c4561b8e7098c74c9cddd5c7b812f987d4059905627cc5b50ba83b029364.jpg",
            "dc2127c75034454d2a6819a66283bc1a13ffe4300c691a68a9e85ad8f73536f5.jpg",
            "5c2683bd8ad6e349e313b75220df5fbcfed3b063c224a2160df72469abef5fdb.jpg",
            "8af91bc278a9e4c6376f3710186648920ea6a36e55b0be80223e30399a4497c1.jpg",
            "37e9869c412142432130616b96c1e70491ccdf4aae9d7df674d024b6136711b8.jpg",
            "e8823409299139ba55c06f5f64547ba59e83fcc309bf65fb5259e50013b5e431.jpg",
            "d9a7391319af2139afe86f97ca4c2913c1f9c286024d461a86626baa514a64a3.jpg",
            "c72a0f0ecad6997406b3701bda27f2cba31580441f3f5c27612da93aa2e1c1e4.jpg",
            "8f1a64a547caf9f8d709b7f31d9a6fcc76e545db41e85355a7fd07fa27a283ac.jpg",
            "74b671f7cd7173f53e2dafcfdf37f0062ebf722b28736e3a3baf760d413c93e5.jpg",
            "ddec2c31d07f906975e0b15203bcb7cdb972ef376eec5923e2d756f3de96803b.jpg",
            "9eadf5525da26a9309816b2e5da805d29bb823e3c61e7bd8bb5ea44d5fe1268f.jpg",
            "1684a634866e28e483cfabe4f7634a4cb431dbc25dafdb7bb1a2abf12d3b70ee.jpg",
            "e57c40e62ac4730edcfbf93fa618b2da0bc7dc7ced9858bf2aa12671a0892891.jpg",
            "21c96284c697fc587f8ef066d0389cf8c6e27c979db6dfaa6e549d776bac83ee.jpg",
            "1745a736e38cb18426aa54fc1a36d1e14383b68c5088d61a223bd9d501365a82.jpg",
            "c8ab53d5b5bf3e8c26bde9d8c91ca2964e642ca19bf35febdae97bf608177885.jpg",
            "7730d5a18d9c671b9ec0826b6240c6ec41c2dd345b0ff4f52ba2b59e5d08649e.jpg",
            "4cf7cab625e5a1849087db694c36fa87c8975751a1350c61c89a4ce5b374fa20.jpg",
            "4c471f970bb1904bc5ce825b2fb46a564c9babb9962d1f3ef0d9bd58ebe26c63.jpg",
            "81d6df8bc2878344b29727dc4b9f3672276bd4e0b358932810edafa234b3f233.jpg",
            "eac6d1470b1e63752a17d48d284bf85ed74fae424217fe8828f770e97b0fb5ee.jpg",
            "62ef485a70ae7432688f366a7d4c67b33107a5ebe7e52845a5a5516a23bdca86.jpg",
            "fdf627b93b561d360656e610ed9d958cbaf767b7858a08044d56da17619e5db3.jpg",
            "9d723a47df42a3345d766ce32fa44101ca6e05a514b7be728e5feccd1ba5dfa3.jpg",
            "c4999fd99b6d98881ace5fb835fd22eec3cc258266395dcb0d17be4eab49760a.jpg",
            "22b442a7e2b24efe69df46516b1b1dad4a43d9d1207324e0b2d1c0d3c7b27975.jpg",
            "3f05655179c6ec25dbf6caf1aa29e9bb4848df6fa1dea1a88d00281706c0f844.jpg",
            "493cdb9777c1ae02a307b2415780af8470d65ff91c99beeb59b868eafc49a22f.jpg",
            "b67b294499b2a27cbf40157ae0907366f53a66856db31ecb7cf559c7a12f169c.jpg",
            "8c2288c394c2809c629ca2dbb8f5d949972e7e80d1437ebc545b5ec681be9092.jpg",
            "f9aeacf2c7dbb96c3cf2d466ad6eede47096d4c55f33d32a36375eb929308278.jpg",
            "2ae27fb4abde055ee7ecaf55c6f9745ba470f330780fb88ffd692695efb5d6f4.jpg",
            "dccaef90b8aab25285150445015f8ba2b358c71a78d090cffdfc2c6ed771d273.jpg",
            "000d15270c5ab763d68b0d9a1217f0cafe17f073c9463e47523095c168c2bb40.jpg",
            "33769aefe642045188d5179fe0589340a144199cd88f52543fa2a75c022bc766.jpg",
            "4c1ab1fe000e77430f259eb0dbe84c13ae644445cd4cec453ea93433239d067e.jpg",
            "b028fc9cf60b3af6dcb20e19915b33315f0de2bc22dfde264b213637f4e01000.jpg",
            "fbb6a1bbd592b62f5df8ef3da506a0516fd0ada2a2554abf86b171bd9ff5a366.jpg",
            "b747a437308b2491769ac899f00741815f658af8f1cbc0338418b0b925a4e813.jpg",
            "c488503ab3573fc243303778e0934f34e83d4742e0712a7927b7385763fb4335.jpg",
            "d3f11aa1164911dd2218129be2281801fe93d948dcd5d6db8c5907bc918f04ce.jpg",
            "aef12ea9fd98a57311314ce0ecdf792bcc2f53dd8def51c52ee0e9d752bcc675.jpg",
            "70fab88c5603fa193dc84de8e50ad9601e10f00dae2abe77fb4665de572f12a4.jpg",
            "fe4050ad574dc6c5273caa7ed6fbb7ef90593b856b59948729d56e354f1bc774.jpg",
            "df8e2d63ba1271960252b58ea4c6780098ee60a2f0207170f2f7dfeb9d6336d6.jpg",
            "3e800cc7181c051ca06193a96a480fef0e6b9059d8ec541ecfbc02f0738f35a9.jpg",
            "c993999c2c4eff181ab25e188d850cb68a69904961c3dd15d7c7f0b35d8f3129.jpg",
            "9bb2c3252fa8d8d272ea9cea7d412cade6214195cdd83ca3bc321fb4ca30bd2c.jpg",
            "c64f42af27bb4e9a6a215513661d6473be736cdc97d9f9e9ad66b97852be4a77.jpg",
            "b2427790f1ceba1e58af8700bd071c12e9c8fd8859f059499a469a3b8382293f.jpg",
            "438fe55aab034056d350abbd3f219f7154a31fa0c90cb9ad8cef4819b053e99e.jpg",
            "a76874fdcc7ba8475f3019a1afee548f1850ac43c1c4b07ef8adcd9046f554c7.jpg",
            "fed2c622e7e07fce0852ba7e1d4e0da9f67d10a0daa25e5772752e57b9acc027.jpg",
            "7f0ced7d31b4734ff6fd599ee6c675efb3cc10d1ae44da0b3bc80b8649b74cea.jpg",
            "8e44016e48814fa80f188cb071d57e4e253c7234add487a5eba9d3b265c81573.jpg",
            "992d426d27493ff5127db599ad9b7864889876fe0d1a59a33e941cc2dd2defa2.jpg",
            "b3de2b1470acdb9e8bc50b3f1e12a4894b6e7c83cc6351b1175d83b22aa86a5e.jpg",
            "d30b655e8cd95f6c084baf9d7ca1acca7ea401abd4e1a8006022ba588632f9a4.jpg",
            "baeb2c3dc42f86c6197900d61e21b47b18f072c624fdce3d7f548050f80d54c2.jpg",
            "2fb1207fec8924fc7039974394b7ce1fb0257b54f65e57d914afe23686e20548.jpg",
            "4a238c1a2d0693946dbd848125b8eae3285712978a863d112e5d54c71b728b63.jpg",
            "d1732e2032454ef9d5d1555042fdd3d6ebaff7420db1cbcee8f3882403f0c5cb.jpg",
            "f29ade4d1c926ed50f9ed35835ef0afab6644c1b413557205355f5c6ed7c1ccf.jpg",
            "8640452f02b97eee8c5eb80c99d9c9ad1689e8392027791ef69f3e2894bafd67.jpg",
            "d9e133d2feda01f2f25210eddde0e66711067e84dd698bfab76b82fe5dd72e5b.jpg",
            "b270b6010a935b55a68a0b8c5c6c26bec9850db5bf8cc80b769abb606fa75e6f.jpg",
            "e61a3847c44f4ecbae386ec69fa635b9b399e2c2f0ce15e287f57924be9157e3.jpg",
        ],
        "portrait": [
            "3ab2e48428f12e2f844541e28ec73dd36abe89f6f171056d74c97f0af735e67f.jpg",
            "630e86d7fdb0a8a914730a461a9b1cb5f087b68396c5d919e4ad78f53d9f1be3.jpg",
            "ffa3e7e0994bbfa9d4622915d2376d9998ba62ce12bbabf8568565c7543490a8.jpg",
            "6161feba487e7073a91ae326d3526ba96952145f3879a0f18b7f228f7b4c94af.jpg",
            "fb126e0d720a3d6b5a73d1088aeff2d75c79d30becf8b99183a802c292e90113.jpg",
            "868276cf2eb5408af4636ac0df870428c64dcc6447409eba84e48a128c6ecea5.jpg",
            "6f9863adcb746b931246d20419a5816e3600b7522aa01bafcb0fb029f9ca62be.jpg",
            "4e1e8b9f0a5867c51f44446db12e43cc283a9cf78b6c2e36acd1a8b297b7d7f2.jpg",
            "8372967f31b11372a993ba911055719218dc6aabe553cacac568792bf6fdccad.jpg",
            "6de6b9fc2e020ffa9097b392049955881ab577c9553bed9ceb316d3d74f15ec3.jpg",
            "fa2675c52a04b073bd206b8258bb121d9585b378f2601846f048098ae95e7f21.jpg",
            "34fa58c0c07cf6ef3d1f4d95c462786ccf2965c026bfcbb4a8a95dcc9d6a7e02.jpg",
            "14096b3af6db65e7a9c0c06b07d21d106ab0cda9ef2fbb2ead452ce394c6f941.jpg",
            "f0ef0169f821372b57ecadff550b6e4a250be91cd54b63af167d12e9b05db2b6.jpg",
            "0a36603a24a6fecd1688f23a0fec70b1a0b3d6e0940b471ef218993540caac25.jpg",
            "f014e0e7fdf854aa682e1d7d3e39dd5a2597809f03eb73896ed67e8d7b5764ad.jpg",
            "677368c1500064084d06cb4746a1118d28f5fae80d7753c34543028d70d66a22.jpg",
            "8479a566d08ddf57278dbaca8c2d549fe021a47a2f2216a881793b2aa6d4b072.jpg",
            "d93720d82ee33e65b92e0151758d7a97a5523d85bfa0e6fe3fd7a3a127bbb776.jpg",
            "ce36418a7c05b875895d04c6e1caf3e676171018a52c3971323698b4d6c47a0d.jpg",
            "cf29a93975433fa8283152765066bf253363a3d8ee0f95f7b2d60fe37e3906b8.jpg",
            "67694aa4ca4ef6efd6057a9306cb8dce7c6b2fd5d18e46541b4b9265152c0a16.jpg",
            "c3668f6ce0d12cdf94dff542816d27f26142252aac93fe1a0657dbec73aa743d.jpg",
            "f816ca8d81a59a68ab85fdc28f7deb4fd87b7ef3d4d9682d7f88b22d85e27a33.jpg",
            "fc6b23093ff9bbfdd6f4e387b118982b213fbbfa0d624600deb2ce69c350ec3a.jpg",
            "5c65af7209efc2a9fd074e22380b0300749372f916fe2d7092d767ee8e295758.jpg",
            "94f8339e5803834a3e743d2b6f2ebd32b425245e1aa740e7a0604debb5fff126.jpg",
            "adad4a33c1110c202ad2e6e2d12457d91651dad42fa86103c39e261d21b378f7.jpg",
            "acb102f55c274096113552f3e70bab4e183fea58c9141414443a46afc65cb328.jpg",
            "23a0eac031ae7836ec421eaf4d98e6b65d8afaea057ffe0b28b2311ed10e5a92.jpg",
            "41b8525879707ae34b4dd92a962d4b1dfb32f0f387a3cd16337cb62582d7b758.jpg",
            "9effb32012c5ff2cb79c81648ec44fcedf1644349f19396d7707e9629554c26b.jpg",
            "b510a04da171ab8da688e212f7a1ec8b31fc07642ca513801d442a8847798e84.jpg",
            "7683c196c7ae128e8d2f2a60310877fe630fd39095749f571ebaccbe47e1f6bd.jpg",
            "2674c70f2afe0d51633980a9b047c48e211719a5609b354695148c767a1b69e2.jpg",
            "fba1e566323a60b55911e650c62bf805782426273093dfe4b82dd64f76b599f7.jpg",
            "76ee81d96e0b52bface9332ea89401e1f370e3ff96aab3804bd53c1eee71b7e6.jpg",
            "0633ee7a6f225fe681a21234e4e7e49fb0e64fe89a0bf309cdfaeecbbd369ca0.jpg",
            "5feca87ef76a3d15b17cf8082fb546042ac50a9193ec6a878eec3d2ba2eb548b.jpg",
            "39bcf1f67cd67e2daeac1f9fb1f31ca64300f41e71183b7f7f8c7b24f43a1951.jpg",
            "a5c0cee1f62b853a74b8da2af94d0d0ff6678916e5f160eeac6fec2d47323c8c.jpg",
            "66c59952f161285151d18c491001937c9cccf92ee0b09e017e4dd654793168cc.jpg",
            "eaa84df8a4d21280e7e449ff104027788352fb9548ed25ed2cd645844644bb86.jpg",
            "3c7d3042cfe6bba6d180742f1d4ac9865c3a0695f695c283f1217f202479a3ec.jpg",
        ],
    },
}
