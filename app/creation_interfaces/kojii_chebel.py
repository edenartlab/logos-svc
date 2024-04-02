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
    lora_scale = request.abstract
    seed = request.seed if request.seed else random.randint(0, 1000000)

    if request.color == ColorType.color:
        color_mode = "soft pastel color tones"
        negative_prompt = "saturated"
    else:
        color_mode = "black and white"
        negative_prompt = (
            "color, colors, yellow, orange, red, pink, purple, blue, green"
        )

    if request.number == Number.one:
        prompt = f"in the style of <concept>, oil paint, {color_mode}, woman, dance, brush strokes"
    elif request.number == Number.many:
        prompt = f"in the style of <concept>, oil paint, {color_mode}, women, dance, brush strokes"

    if request.aspect_ratio == AspectRatio.portrait:
        w, h = 1024, 1536
    elif request.aspect_ratio == AspectRatio.landscape:
        w, h = 1536, 1024

    control_image = random.choice(
        control_images[request.number.value][request.aspect_ratio.value],
    )

    control_image_strength = 0.95
    guidance_scale = 6.5
    negative_prompt += (
        ", ugly, watermark, text, tiling, blurred, grainy, signature, cut off, draft"
    )

    config = {
        "mode": "controlnet",
        "controlnet_type": "canny-edge",
        "text_input": prompt,
        "uc_text": negative_prompt,
        "lora": "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/431ff8fb8edf1fcf8d1bc1ddcc2662479ced491c6b98784cdb4b0aa6d70cd09c.tar",
        "lora_scale": lora_scale,
        "control_image": f"https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/{control_image}",
        "control_image_strength": control_image_strength,
        "width": w,
        "height": h,
        "adopt_aspect_from_init_img": True,
        "guidance_scale": guidance_scale,
        "sampler": "euler",
        "steps": 42,
        "seed": seed,
    }

    print("THE CONFIG")
    print(config)

    image_url, thumbnail_url = replicate.sdxl(config)

    return image_url, thumbnail_url


control_images = {
    "one": {
        "landscape": [
            "7bd9892213aad252f91a9c1a4f678a0ef9c9060682c5de31780ebbbaf751afa6.jpg",
            "b3e536e51c7f3eb5b256f8e3bf740c1a38e9f9c4f8a7e4a85f461b0756e5013a.jpg",
            "bc167fd234c3c64cee3c575d08f70a1cb4c294cf3f8cf0608225ec6957fe6b07.jpg",
            "0a3ec22a9c01aae19bbbcd844cb3a09b9026fc142ce475d1a3c0acd4490e7f95.jpg",
            "cdc9b1538c7ae8e0f5937ada79290a1fa686ae6de897e615a6b480f24f78b639.jpg",
            "32c8821632ec29bf076c81f95f3c8c6cd8cb78a0f3e23eec685ca2fee2c993d6.jpg",
            "6dffc79ec9a1ded80eb1c4d344614f531a7d9f179733e200411407ebe024b74d.jpg",
            "02d8c48b76747f5ba05fbcc7e259e123eb75d606cceb8becdcb23b59be7169bb.jpg",
            "f78899a5676c61480104161564e0f2b47abf32bc537d4f1ae0c4ecfaded7f339.jpg",
            "4444eee464e11f7bbd9a8fdaeec07360368fc30ab5973cc83d9309c13a19185a.jpg",
            "5ab8cb1db96f932d69221d91ed89f1703d260f6d99997d94dcbb8fa8192c6c2d.jpg",
            "8a6f3aa6ada415f0e1d1ad0c0590d7baf8fe0542af6da88514daf9644cd76062.jpg",
            "aeb8dd4096082e9b2ec38e74626f9258efdb04ae7b75f1fa7afe3a70c6a3cb93.jpg",
            "2baa2427f7994ce185ddadf1331e800d208fea2b68e5c5d43b56acad2194f715.jpg",
            "1cae6e6b15c9c19b7317a6c899fdd8c8a9802fdfc9aaf61acc160be31216aa75.jpg",
            "d63f5769217a8b5d071294b0a14f2e6d34f4b4a79397ae062810841c36759a82.jpg",
            "cf7cb38faea5ca81b970564282d16f3ec56112ca0b7499b3af9167b0ea6e1b9a.jpg",
            "008816a11d388d211c2dc734577d80465ff3719864874353c90d24fb9046a969.jpg",
            "d855ea3d1f62ca8f6c5eeef3349106901084e45c94afa5426350c71bb3e7b2c9.jpg",
            "ff0528b4b2b64c20f80a6c047b85f80de7734c5ada6444165199ed513fd275c6.jpg",
            "520b020c7ac04979eb68724ebdb75ef4cdf7d21af9ff7b4a34e4a277958aba68.jpg",
            "5a8bc0fa965fe4b6421e4a3d76f52213f2635d6204c5ad2cfcd92fc4590d9a45.jpg",
            "fa37fcbe28e6022ff9c238313f63be037946aeacffb9d2a9b0af40956b755bc2.jpg",
            "8d59633a3d5b2d92ee3c02c6dd4db083f9ba8b515c0ba2a521eb91eb15cd31bc.jpg",
            "11ac91c70f892a0f393a1b773d1251d099bd7724814417e4f8ff808838423a33.jpg",
            "f66d92392f95b970c64013210bc29aa5a1ac0e385a81dc6827c53c1825237689.jpg",
            "f6a9d7a2c3cbe19081644aee5f7f03ad85f9062f06ea647658006e8f4d313e5b.jpg",
            "9ea9b48da25670cf1f3027095c52fd5a4fa076dcec15d54fb3380ad4225ddb24.jpg",
            "d3979bbec7f2414e5e8643a23e45b4676b9016bb7944a5ee9ab3286ff715621e.jpg",
            "b86ebebfa023d776cf66f8117aad03032344205ad344a2f84180da96879af09f.jpg",
            "75d5b41c26e45573c48b88f42901dcf9eafbcf5a7b6a4e6ac9a70b819b2a54af.jpg",
            "b2433891140cbc62828954fda4f8fea78ed1688d5b72f5bd73efdfce50e60c7d.jpg",
            "84a80e2ba46bfaac52ce6ab47d6b74e86973a8cbe9b9a0e0a7750f7a14e9eeb7.jpg",
            "51ffbeef0e328bd389d0a995a9affc5d99ecb813e6ec3e7f92a8d2d65223524e.jpg",
            "962212572adbc1c2431c15e743c3b7a5c476f1941ee2ac7a991829717073a675.jpg",
            "6da8ea6e89ea912f02d9dee1603e597099990e1a15ce7ddd39767c04ae7791a7.jpg",
            "cf7638aea862c976144966a89d07c14515385cb7099b675421b0a0df7b8d2a42.jpg",
            "3232bbf53d61231b286102f33d0451006ed31849e2474c58093b6fe947631d19.jpg",
            "6f75af9697aee84680b55952923d161ca79101d61942888673f6e35a424b0298.jpg",
            "8bf9d95c87c10243a18171ccf13d3ef4ca300f33699b1258f999165f79c1faa8.jpg",
            "ec267b2936503f3af56cd16b0b5af4e13966097207564cb77687f44f0f23f439.jpg",
            "7327928fd90a4b8306ef0bd89f8b8b8927122ae31f4bedbbcd4ce76474084bc6.jpg",
            "a9ebfa67e258c7bb2df5ffb3e9fff837dc0228d34a1528052c94a57b5784ac26.jpg",
            "7bf87d3df1348ce5a850ac1cec5e2ccb37b6853e6233ece97d96c1f5e35e64d7.jpg",
        ],
        "portrait": [
            "bb9d0983e89491dfd18eca8f7157715f19f6513ec56f031398ca1786ce75855c.jpg",
            "fe8aff11ad70f030a093b25142b9a079764d538374ed128f00250f5b5af6ec73.jpg",
            "2e4a118c0d7eb7147c35104ab56a69d4c8642927be4f96dfb402955be2603053.jpg",
            "b703398037ff1a9b2c03e3bb6e35ac0f5b50f087b07ed76cdc885af8cb60ec91.jpg",
            "ce6753f069d4615e415a53d63c09469eb0c749c459107b02d25f67bd8bc1f97a.jpg",
            "dea5510c9f78ff47e38f3aa8a5799874448abe6024ebfa4ad377aaf4d4308adb.jpg",
            "3c50e2fd251325a273f9aad6bbcb382b1be674299b1fe55be6bb3e9b5ad04ca0.jpg",
            "a194cf9d545f9965be86bdbc6f34b9b0b74546a04f5fa9760bda511f7a97fb7c.jpg",
            "a762dcd6878ec33edc76632bd777de18f825106cba0e5d6c6d30d94b526a05ea.jpg",
            "9d32e406190afab64254db9b2d59d64a5a63ae6e6c53d65b6ccc05e0736c67e5.jpg",
            "0bbcd41d3c972bfd15f4b83a9a63ef342c178f8a38e7439048510527532f3cba.jpg",
            "915d636c728c0d15119fca38d1296c6d240045df31691d9ab34debfecd6d3833.jpg",
            "08bf6de26eb97d66cea3fc40a87a22cf9e970c874263b45a382c57820fe6ad4c.jpg",
            "cf06c74c5dae4e08bcf98670dbe7d71f1e66574d35a1ea80244e3353f3a8a6b3.jpg",
            "d7255857bba8c7cfb3f3f4104b284d2e0292ea536716eea74a3e4a247077f396.jpg",
            "43059dae688b95425591cd22a7e6b00f3546c4cebfd6a3f8b7a23a007402265c.jpg",
            "5be4869cedc73bf35a9a1d311880793405b1b929c2df1002bfadbfcef119769c.jpg",
            "34f7be53ddb584ed7d3afa2f2c3cb68ce20148a5af9f2a39d6e05ac48c5bff64.jpg",
            "afdf69fccc18b9659fe5a229511fe4dbc30622677e3fdf8bfe2276b0b02ed7b4.jpg",
            "9947627548c00e8b82acc8f0dfc56c022cdee1b9192aae8d840e1c79b8e51424.jpg",
            "294eb7357f5cfc1eaaa3a8cb2062b84b8db1e368931b67fd8e1148e77726883a.jpg",
            "81cff9ddd2f835bf6ca3725229f508b8da0976b9d7a092a06bd93fdeff56ee5b.jpg",
            "debfbbd9c90ceb3474c3bd19e4ecf7c57c958e90cd25b915ae085b366a8db24d.jpg",
            "568d0b3deda19a47dceef35d4527d5a9d4e61cfa9782447841ce2cf8298c2f62.jpg",
            "3b7556d1c5aff809b67ea957c85b304727f29cdaf62568e2713d9d493014aba3.jpg",
            "a79bd60a069459b5c29bd2bfef44da077fea42dac02b97d1ff2d516afa24a10a.jpg",
            "b5175e269a155ca86e50aab356a2a9bbbc3b5f5848bdb74edbfda52f8d5bdff9.jpg",
            "7ef81b92d7602345b2fc2d1bde52741f453f82a0a08c3881281d9a928a8b53fa.jpg",
            "3a17448b0f54cf4e6381cc934731a2734af31debe443e14a6c9dd68fbd2d2db4.jpg",
            "1b19b139a447fecb2a4692d1541faf5d9465f1c9370b683ae9bfaec43247f39a.jpg",
            "565e6463e2dba76377b13dfda546cb76b8bb2eb7d7228f7e2191ef4bf6f6a721.jpg",
            "5badf0e3da37b5945de15a04a5ca1d05bcb9e25bf50aa52b00580604cdaaf326.jpg",
            "bba9cf8d6b0b2afcc07d4e286b1897285bb69428a881b42815a1127c9a579053.jpg",
            "1976f2c658e1672eaf54c466a3d5d66bcbacd1fed259e850dc597abda0d23143.jpg",
            "8327b4776603bcd36cf76d60389b71413fe31cd838e243a63db791ab4f1c1851.jpg",
            "1142850a7535b20cefdf36379474e1da06986e073c01ba9c6ab2e28ebf0bfba8.jpg",
            "3777f4bab36ba99c71ea3ec71022ee30045f679fb4c088e9743c701606bd35f8.jpg",
            "296476fd4148b07f6346417d921047a48e7c85656942d0e9902645924339a7c3.jpg",
            "0859e28957c571d0775aab681b710d1eaa58a2de8effcde104093829108ab141.jpg",
            "8226a0f776654e02c36fd0eba51f595f8ac7132984b36a1c2802a6aad6060dd3.jpg",
            "873fafbf9bdd288aa3b20fc22fe7b38e896bc6874722e1ad5b9dadfd51f2452b.jpg",
            "d6cf98d0907a555b3ac88db1e62fdd0a509d9738179daf307a9460e0993fbbbd.jpg",
        ],
    },
    "many": {
        "landscape": [
            "05641ef30421cd6a3b325a8a33500b22c56ff7f2b664ac8eba169c48fe259dc2.jpg",
            "c2042054e38cc20eaec09e19fb601e9b78a12d1a04d7575247316ddfbd392951.jpg",
            "b61676aa9ebaf41f5c96a3b8304d84e29717ec897aff377dda1a6f8291d461a6.jpg",
            "b6c4b00df3909712cf31797ae4158332939b35a2b5c5de1b8bcddead81649fe5.jpg",
            "5b077b165933f80dd63000416a90d688310562f61ae9322fcdbd51962630c4f3.jpg",
            "d05861f351375141cb83d12e330509f2bf12af3def333ee3537c07ba046cb370.jpg",
            "dd1a75d46c555219a4f33dd4322b9a2c98e8ec4c9a2d46d4b96de41e8f210d81.jpg",
            "ad74b11bb850ae0e4ce1fc258db0f4f206260103ac9103d75378240325019042.jpg",
            "c281264ecac3352179406305110faf63d8f4ac8c4a3bfda17b7e5bf9a29a04ae.jpg",
            "ff1478b21b0d9253fdc9a7513f8a48163ef6e8bdd74cd29b0d14efe0226c946f.jpg",
            "089ad34db78dd4ba40a898fe5f182cc78e4baee54720127fca8b83b162a35fa7.jpg",
            "1924e6677892c41b8bf5faa53a94932f415c523e3e8252a9c6e9e647eb532540.jpg",
            "728a4d7728b1b954df70d34de20af6a4e0d626743fb1cb3a287e94a2a265c132.jpg",
            "c5b2ff6d278ae1ba1bc73577ef5d104c96f24ce8f01cf2870459b15e39aa621f.jpg",
            "f6d8fcdc4973dd7920672cbf0e2e6cb4353024d39af986cecd00a5923443cdec.jpg",
            "71f98760c2e99777513784c2058d7287ec1c5d91bee9584fc261ac965cae10a2.jpg",
            "58bbec94c6c08179576f57861dc1476b80133963df9b9ff0aa884073ee315d36.jpg",
            "4729eb99bc925336c78391fffd6f873308117f546737accb528e9e3825865e97.jpg",
            "3e824c591706940669b9e40d7aa2b987149c8eaa0650a31c984409d21278cdd3.jpg",
            "51529aee4dcd95f70bdd79eb4e16544515905ba61a2e1e4fb6db74ea22bef969.jpg",
            "3de238ddb2c8041688b49b23bf70e18507738caa68e7d106d120d6e45813f049.jpg",
            "dd0653bcc4572efd0c12627cfe48c810c99a57622eb9fb1b52ec2299df813678.jpg",
            "73cb10c4c09c1bf0d4723cb5a32aaade49f081cf9677db27f6b2bdeb64722b0c.jpg",
            "b6b9661466e37e4d40d6548fc031983c9dbe83f5799d8fd49c5b199cd9cae468.jpg",
            "25bcc021607aad141184ae75f0dbc4e78ccdeb1af04a0349d57f06c70e9c2154.jpg",
            "156d472ccc9f2f0326cb2189e4e69e0434fce43696904c60ec42bbc688cfeab6.jpg",
            "e8631010c2c0fc42614565245ec081d1b670d9444cfe6fbea89ba389873298bc.jpg",
            "4ec00fe8545f42ce2e15b11e741d3d7103ab5c3a8d188a9bd177fb5706ae35c9.jpg",
            "c746a655f50517d01fe02331a844613efe62e2f6b5e26ad208cdeae624a84cbb.jpg",
            "d862bcaf3473945aaac288d007b7872d9e3c2514256ab8f9345d40c0b21a06ca.jpg",
            "68c1e661c825bd4a0f891a6a02e20037faedea36b4c02466ee8364023761e882.jpg",
            "da83313c9967f80ffa00a20a22906fdca020e5c6f5f27120c099c63ed70c217c.jpg",
            "f464606e7151831b1aae45ddf8a2113b8dbd8b2ae3c1ac84fa7f7b060d9e3e55.jpg",
            "4188eb3b8b9644d6f4f2b43f3ebc5f0fddef228b26fc299bbb88105f9b6ab1ce.jpg",
            "06f66eda10a8625911366266f894bd80cec12a42dfdc858b3a1f120dbe7a72e6.jpg",
            "bd9c8dd95733dff98d05a5f79aeb8e47d11cfc11f9f81976deaf5ec88cac93cb.jpg",
            "8dc132ab7c3fb6ee1a9a58d1381349433e15bbff288f98fb4d93dd41c143067c.jpg",
            "a0623764df54c930aaab12081af85bac527a7a4d63fb93297c7872f961ffcd79.jpg",
            "e0f45fa9d5243be43662faa9273799a9ebc8bc83f36fe51e5096e42043b6b633.jpg",
            "5f7c73ea5acf1fcbdfb4c37d1132ab54e4554b7d71ae04e38caf004d9eed8ae1.jpg",
            "cc7563217d8f3b3afb35b6b6556fb7eede3efe935f07d714b65cdac72e9e811c.jpg",
            "13b1cbfb97752b36ff4f0948dc2c82643f5404bc71269e0e32b89b10665b02b4.jpg",
            "163f32cb04b95a761c66404124e86a68d3e5138e65c30fdd00b53e07d080b4f5.jpg",
            "354bccf88468e0f06ea06c973ecc227a32bd2ccd3dd7f40e47b6a4524ab7ee8c.jpg",
            "b93a172dfc2932c48c41d0a69217656c654dc8b20e40dd24f2da2ee69babb794.jpg",
            "8696872ae4710d6057eed1847fef5a47ea3170134c536dfa8ff9827ae48d03fc.jpg",
            "968229c57062378ef7a066c9d6b5216dfce6f68f7718897bbfe2f440802272dd.jpg",
            "582f4ab218aeb6d372eb569dfd85e2402a03a5c57b6f7c551720f4d372f57791.jpg",
            "9a042652a4522eb7062c0868f1fb3e986f27f32bcb4ec3d44f468a695b58d3db.jpg",
            "19c6e813f39b865a0fab018c561f94ceff72cbbbe760d298b3837edc0977aff8.jpg",
            "8a9705f8d278606e4de21a855d899d8388f459df065d9b1cfece1810a8c9c2ac.jpg",
            "be61c3b17109d88cdb3a53301d1dafa248d313a27b751da14ddf40631442e6c6.jpg",
            "d04315142f95a53d0aeb929cd8ef977dd871b12256e2ae654ebc99b7c356df5b.jpg",
            "06ce78c9f3677a201ad456c0d90f2cc4a856547991d3a5588f4fd28ce9fee3bb.jpg",
            "45fea6bad88dff18fde37b144ecc387b86fd26932d88cfcd4c65e8b586c97b86.jpg",
            "87ea173c679785a160710fd1bf04ab9bf9b93dca01a4c479c86ea9c43e2d5f76.jpg",
            "33c0e6456fe7a97615db555995a76d0b39de2346ea11298ec225ebb16381f42f.jpg",
            "e0c305bbbe79a7d9553d41d0fc2bf6fdb99d559bfbea73dbf7ab482cdc054d35.jpg",
            "d8e0f64d379dbeae6ebb16d128cf3a020f14d7392e07907e74d9c8bc3ee552af.jpg",
            "c210d6d99e6d81a96d681349983e9f30e624acb49b240a938bab256eaf3b6e22.jpg",
            "852e2df979af0ca1d1c01eced84db84aa73667323f6c3252029847fc4dd3da49.jpg",
            "a256cbefe27a435c9be482ca6c1cfffdd5093c681fbc9abc518529690fff77ee.jpg",
            "a34d74d2c481189eba7732826f372fdbaf83b01a3fc61069dd2ea5ca252ec208.jpg",
            "8e366993f71e6c790782bfdc6242d57f60d5e067b11927c407f75923a293e0b1.jpg",
            "b220d46d819d9f032833e1557a5e92cc4e035fcfdd2d9d779aca7ff48720b17c.jpg",
            "97d8d3be8baaaefc27088770b3cdaec45b1b9d66a5b066fd8b17c14ad64fb595.jpg",
            "01eb1ad0b6c4b91fefc45376d7d1b696809258e4a46b4cdbd736695359a7df2f.jpg",
            "0c652983da87188842dc0f7bb1b96bc94263c8efdb52b5b33b214e235233b3f0.jpg",
            "6c6b42d7252586af098e828db8a033515ff5a734078d2d37882fa2e1193c7e0a.jpg",
            "c3dcd27ed77be77be101f7a57d83e069bba4a8622720122eb90d45d6a88ff8bd.jpg",
            "b809c72bc4e20d979811a16f830e412418c0cd93e4fccb93f3316116f83f0cfe.jpg",
            "632615c4222e05010474488761ab0c78c5215e6c9eb0f7ce3b2d92766d34248f.jpg",
            "0b68c73f2375ccf8ca8a93012ad010a6d13052bdf390ff0e2a0a5e178cc89d59.jpg",
            "1e9f3b322bc12784ef49e47481ec1ecd3d0f163c98692436e42ee80c615495f3.jpg",
            "3a7ec5965c85d68c6e603dad8372001d3ab9adf974a8a44d5e286fe87d7b603b.jpg",
            "f18334e241198b2ac25be1e80fffefae64f59cf936b9e9998521f77eb5c21df1.jpg",
            "bd68d4ebbe38f4990c6089de669994948c1c41c504a9031bf53b2777482bb01c.jpg",
            "d845ad2ef885883457f837b6858982e99125480b8eca56d6c87887e8ad1b2429.jpg",
            "9232e5f090a9309f09ba7f41981d8e247ffd018f86166a62b4b5231ac54a97ca.jpg",
            "3a73caa7212ea590aa6d9d018d1507ff6dacc0c564ea461d15752d860b9524b9.jpg",
            "6f8967985eb5d9fb4add6b942b5f9047a7c89bd0be0877a345afcffe2c8b160c.jpg",
            "3e14e6687fb4ad24ee763bb9c85753f394a99d7eefb1b01ab7a4943d3f9d8d41.jpg",
            "3b21135248a95cbf4e011f214fb7552d0d5d30dabbe0e7df6e8b1ad22a0edc51.jpg",
            "c89482acf334da6b1bbd4700eee7846f21c7a99c05fe3585fd19aed4251d8932.jpg",
            "a3885de0e4c1a2768c06ad48bdbca21b4c1642ff2ed2d3624e31f108eb7dc612.jpg",
            "a4c00ea9d3e3fefeed2e8d3cb3c3620f4ce95788ce2b297161b27bd66312b183.jpg",
            "4340dccfe5d6cc0c58257bb562984b0aea2001021b2bd2cdd8b1636330a19560.jpg",
            "7420054f462c6b1ca34205c90c031c631c618e8b56efec6e77179db99395073e.jpg",
            "12cfa907007cba10d71ef01a7003fb14b8759da0fb05d51e5d6c695d1d88fe6d.jpg",
            "bf1eb9ee9c52995d3c722e4bd8d6c82a80aa493404ce2f38725ba61e9a50b494.jpg",
        ],
        "portrait": [
            "276da8f458841b376269f6537d703aecb5848158ccf5b84671c0a62a3d7a30bf.jpg",
            "bab121cf00d898d783c998c2037d15ca8e52fa2e8d5d1a4e9dfdaf1b8c0bffab.jpg",
            "00c83ef50e52aaf3744e11a9a7531d5adcf8730a2be5eab343e9d02131e460b2.jpg",
            "a7138efeca57d652816f92583359d5058840b2525f19b7809eb20386d115341f.jpg",
            "d112bb812787ed46408a30bdc153e9646901223f077f893820b789ac4dc79475.jpg",
            "3ad93eaaeb5a824525cc4aa3234cf86e7a566a21b4cc605a1b1c7342f68bdede.jpg",
            "bc0cccfc19ce432bc758cfba2181a84ef313dacb8fb9464e0c4daecea9c73295.jpg",
            "0c54668d3354bbd8b340813984c579b0fae5659dc1210a2f5bb6b6af39602ebb.jpg",
            "8f7cdf7684a6b846e9389bee5cb820eec0e69b02c05d89cf8a4c930c2f70ef26.jpg",
            "c95e641fa2ba49458d8204cc3df0fa6ee9734896265acddc5688c0ac074ef713.jpg",
            "886bb33fa2e797473becf227971c9274c8d9b70bf398da3e7e908ec4a81df41f.jpg",
            "2a49c3f36c077439838a07a35ebf8a26dcb57b563ad9b78032e665b72ccfac38.jpg",
            "05dd446c74f7dd04f805144ce163ed40c37e615fd0851837fce6b965a6f83ace.jpg",
            "35a24c0c4e080efa77a7000d1bd5dbf3e7ab397d49c11e9f1302269588b0c9ec.jpg",
            "6f9a292bbe13276dfdfeecf608c763ca6a58ac7b0cc93038e9bf0ee1149cc63c.jpg",
            "41d0accf0e06703499d690a13a227a45eda8a69e7cbc0fb3e390716e6cd62276.jpg",
            "23d137f0d638f749e8f4d79741c1e6fee155379626e788f970f1cd48a3f4e9d2.jpg",
            "1514de8dc90e3dff7270699e1c873f314491b17f3bad1581b1422438e4c473b3.jpg",
            "6f7f4a1a3e7582d19c49d31e4a80aaef3aa7c57629cbbc7de098a2ece70f8001.jpg",
            "1e1509d548f8e6bbc0ba0a52af856fd5adc5e71805e31c1420914a3538ac8c66.jpg",
            "8fa1358c6ed1fa70f67f2c2a75032d431bb948f2c2badd7d7bf5100106946ed1.jpg",
            "d554a32a0d481a6b8229239378583596bc7b648dc080085ef30c24ada95a7842.jpg",
            "d14d9b2869cfb891dd3863e7303094c599449c834b9946af4e2d7e6cdd634716.jpg",
            "c714150314ca54fbcb077f465c0aca77e34cfcb8353c1511fab81a626548aba0.jpg",
            "4deb6d90c4ba0060591991e23d0250b05d1dd89dbf4fa377add1c53f9c03d4eb.jpg",
            "198cd903c801fd36e84a6f17cbb3721a9350e7c508d4850e4d1ac66042edd761.jpg",
            "9d56a26c49ec07e1bfe0d561be3242b81b1b46099ec48abe226efbaf3213eaa4.jpg",
            "9397b3ca92defb29cfe575ee52e7f27301a95d8f8fe3e5289401866ddc7e8e33.jpg",
            "50d7ae5df425bbc30c9f4cad711c05e444ac692961f298caae063333ecbcceca.jpg",
            "5b438777bf0684d3b9ffd9b369b0dca7b7c71a0ac985f161158146fec9b1eee0.jpg",
            "06e08abe7113a0dac56a9ff4c4a9f01271bb34f68bd0663689652c5026db5045.jpg",
            "3db4a5246b3b4667de126b689763720bd48866f3ab81fc0fc233dea5759a2c39.jpg",
            "6f3d0a1b111f850650efc9798de985791a10e339c780cd4bc8b71ab6ce2145ba.jpg",
            "e4a15e6b861ececfbe19cfac7d772f6260a0452de15a980ecd93baebfc7ebd25.jpg",
            "436f5a8722ed0166c22a6463902d4a533b67cddddecade1c336a90d87be23793.jpg",
            "5d7e6ccbef63a704ef144ee495a04b802c03e5168aad20003596385ebddd063c.jpg",
        ],
    },
}
