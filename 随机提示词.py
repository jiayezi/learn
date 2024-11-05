import random

# 主体
subjects = {'boy', 'girl', 'adorable_girl', 'child', 'animal'}
# 衣服
clothes = {'cloak', 'Taoist robe', 'chinese_clothes', 'hooded_cloak', 'shirt', 'hoodie', 't-shirt', 'jacket', 'suit',
           'dress', 'skirt', 'miniskirt', 'pleated_skirt', 'jeans', 'shorts', 'short_shorts', 'hot_pants',
           'denim_shorts', 'tight_pants'}
# 动作
actions = {'leaning', 'leaning_forward', 'lying', 'posing', 'jumping', 'running', 'dancing', 'walking', 'sitting',
           'waving', 'reading', 'sleeping', 'flying', 'writing', 'looking up', 'looking away'}
# 面部和情绪
emotions = {'smile', 'laughing', 'surprised', 'angry', 'sad', 'happy', 'crying', 'sigh', 'gloom', 'excited', 'frowning'}
# 发型
hairstyles = {'long hair', 'short hair', 'curly hair', 'straight hair', 'ponytail', 'braided hair', 'buzz cut', 'afro',
              'mohawk'}
# 配饰
accessories = {'hat', 'glasses', 'earrings', 'necklace', 'gloves', 'scarf', 'bag'}
# 构图
shoot = {'close-up', 'medium shot', 'long shot', 'upper body', 'cowboy shot', 'full body', 'wide shot', 'profile'}
# 视角
angle = {'from side', 'from behind', 'from below', 'from above', 'from side below', 'from side above', 'dutch angle',
         'tilted angle', 'dynamic_angle', 'low angle', "Worm's eye view", 'top view'}
# 环境
environments = {'indoor', 'outdoor', 'street', 'urban', 'desert', 'forest', 'grove', 'jungle', 'grassland', 'field',
                'beach', 'riverside',
                'village', 'nature', 'bedroom', 'library', 'bridge', 'path', 'town', 'garden', 'rural',
                'wheat field', 'ancient temple', 'futuristic city', 'pond', 'stream', 'park', 'flower sea',
                'field,alley', 'lake', 'underwater'}
# 光线
lights = {'side light', 'backlight', 'rim light', 'cinematic lighting', 'moody lighting', 'background light',
          'available light', 'soft light', 'sunlight', 'moonlight', 'spotlight'}
# 镜头效果
lens_effects = {'depth of field', 'lens flare', 'motion blur', 'bokeh', 'silhouette', 'Vignette', 'fish-eye lens',
                'tilt-shift', 'swirly bokeh'}
# 时间
times = {'dawn', 'sunrise', 'sunset', 'dusk', 'evening', 'night'}
# 天气
weather = {'rainy days', 'cloudy', 'foggy', 'snowy', 'stormy', 'windy', 'clear day'}
# 色彩
colors = {'monochrome', 'gradient', 'spot color', 'red theme', 'orange theme', 'yellow theme', 'green theme',
          'cyan theme', 'blue theme', 'purple theme', 'pink theme', 'brown theme', 'aqua theme', 'grey theme',
          'dark theme', 'pastel theme', 'vivid theme', 'neon theme', 'muted colors', 'sepia tone'}
# 季节
seasons = {'blooming spring', 'hot summer', 'harvest autumn', 'snowy winter'}
# 风格
styles = {'realistic', 'oil painting', '3D rendering', 'abstract', 'impressionism', 'Watercolor'}
# 特殊效果
special_effects = {'glow', 'sparks', 'magic', 'fog', 'reflection'}

tags_group = (
clothes, actions, emotions, hairstyles, accessories, shoot, angle, environments, lights, lens_effects, times, weather,
colors, seasons, styles, special_effects)


def generate_prompt(subjects, tags_group):
    """随机生成一组提示词"""
    sample_list = []
    for tags_set in tags_group:
        sample_list.extend(random.sample(list(tags_set), 1))
    subject = random.sample(list(subjects), 1)[0]
    random.shuffle(sample_list)
    prompt = f'artistic photograph of a {subject}, {", ".join(sample_list)}'
    return prompt


# 生成一个提示词
print(generate_prompt(subjects, tags_group))
