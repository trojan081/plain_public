import json

NOTEBOOK_PATH = r'c:\Users\artem\MAIN\projects\plain-public\data\urban_plans\EDA_and_labeling.ipynb'

with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

def get_src(cell):
    s = cell.get('source', [])
    return ''.join(s) if isinstance(s, list) else s

def set_src(cell, text):
    orig = cell.get('source', [])
    if isinstance(orig, list):
        lines = text.split('\n')
        result = [l + '\n' for l in lines[:-1]]
        if lines[-1] != '':
            result.append(lines[-1])
        cell['source'] = result
    else:
        cell['source'] = text

def replace_in_cell(idx, old, new):
    cell = cells[idx]
    src = get_src(cell)
    if old in src:
        set_src(cell, src.replace(old, new))
        print(f'OK  cell {idx}: replaced {repr(old[:50])}')
        return True
    else:
        print(f'WARN cell {idx}: NOT FOUND: {repr(old[:70])}')
        return False

# ===== CELL 6: apply_labels docstring + inner comment + print format =====
replace_in_cell(6,
    'Присваивает (l1_val, l2_val) строкам, у которых:\n      - l1 is None  → строка ещё не размечена\n      - Text попадает под strict (точное совпадение) ИЛИ\n        non_strict (вхождение подстроки) ИЛИ regex\n      Пустой список → проверка пропускается.\n\n    Сохраняет CSV как NEW_REGIONS_in_progress_{section}.csv\n    и выводит статистику.',
    'Assigns (l1_val, l2_val) to rows where:\n      - l1 is None  → row not yet labeled\n      - Text matches strict (exact match) OR\n        non_strict (substring match) OR regex\n      Empty list → check is skipped.\n\n    Saves CSV as NEW_REGIONS_in_progress_{section}.csv\n    and prints statistics.'
)
replace_in_cell(6,
    '# Защита: пропускаем уже размеченные строки',
    '# Guard: skip already-labeled rows'
)
replace_in_cell(6,
    'f"размечено: {total_changed}  |  \\n"',
    'f"labeled: {total_changed}  |  \\n"'
)
replace_in_cell(6,
    'f"осталось: {total_nan}  →  {fname}"',
    'f"remaining: {total_nan}  →  {fname}"'
)

# ===== CELL 12: print =====
replace_in_cell(12,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 19: markdown description =====
replace_in_cell(19,
    'Улицы (шоссе, проспекты, проезды) - границы - кабели - карусель - котельная - рельеф - "строительная площадка" - флигель - Спортивно-развлекательный центр - КАЧЕЛЬ',
    'Streets (roads, avenues, driveways) - boundaries - cables - carousel - boiler room - relief - "construction site" - wing - Sports and entertainment center - SWING'
)

# ===== CELL 93: _pipe_exclude_re inline comments + print =====
replace_in_cell(93,
    "r'канава|'              # канава-0.6м",
    "r'канава|'              # kanava-0.6m (ditch)"
)
replace_in_cell(93,
    "r'цоколь|'             # 112.45цоколь",
    "r'цоколь|'             # 112.45 (foundation)"
)
replace_in_cell(93,
    "r'авт\\.ост|'           # авт.ост.",
    "r'авт\\.ост|'           # авт.ост. (bus stop)"
)
replace_in_cell(93,
    "r'^наст\\.$|'           # наст. — только целая строка",
    "r'^наст\\.$|'           # наст. — whole-string match only"
)
replace_in_cell(93,
    "r'крест на камне|'     # (крест на камне)",
    "r'крест на камне|'     # (cross on stone)"
)
replace_in_cell(93,
    "r'горизонтал|'          # Сплошные горизонтали...",
    "r'горизонтал|'          # Contour lines..."
)
replace_in_cell(93,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 104: markdown suffix =====
replace_in_cell(104,
    'пробелы, запятая, / Р, две точки',
    'spaces, comma, /R, two dots'
)

# ===== CELL 109: markdown =====
replace_in_cell(109,
    'TEXT от 2 до 5 чисел',
    'TEXT 2 to 5 digits'
)
replace_in_cell(109,
    'в зависимости от слоя',
    'depending on layer'
)

# ===== CELL 110: print =====
replace_in_cell(110,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 111: markdown =====
replace_in_cell(111,
    'TEXT от 2 до 5 чисел + буквы (латиница)',
    'TEXT 2 to 5 digits + letters (Latin)'
)
replace_in_cell(111,
    'в зависимости от слоя',
    'depending on layer'
)

# ===== CELL 112: print =====
replace_in_cell(112,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 113: markdown =====
replace_in_cell(113,
    'в зависимости от слоя',
    'depending on layer'
)

# ===== CELL 114: print =====
replace_in_cell(114,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 115: markdown =====
replace_in_cell(115,
    'в зависимости от слоя',
    'depending on layer'
)

# ===== CELL 116: print =====
replace_in_cell(116,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 117: markdown =====
replace_in_cell(117,
    'в зависимости от слоя + ДОБАВЛЕНЫ СКОБКИ',
    'depending on layer + BRACKETS ADDED'
)

# ===== CELL 119: markdown =====
replace_in_cell(119,
    'Слой "Code деревья"',
    'Layer "Code деревья"'
)

# ===== CELL 121: markdown =====
replace_in_cell(121,
    'TEXT люки / кабели / пнд / пэ итд.',
    'TEXT hatches / cables / pnd / pe etc.'
)

# ===== CELL 122: regex group comments =====
replace_in_cell(122,
    '# Материалы труб с размерами: ПЭ, ПВХ, ЖБ, ПНД, кер, бет',
    '# Pipe materials with dimensions: PE, PVC, RC, PND, ceramic, concrete'
)
replace_in_cell(122,
    '# Кабели и напряжение',
    '# Cables and voltage'
)
replace_in_cell(122,
    '# Статус люка/колодца',
    '# Manhole/hatch status'
)
replace_in_cell(122,
    '# Отметки с префиксом',
    '# Elevation marks with prefix'
)
replace_in_cell(122,
    '# Габариты: 2х75, 2х150ст, ГНБ, обойма',
    '# Dimensions: 2x75, 2x150st, HDD, sleeve'
)
replace_in_cell(122,
    '# Газ\n',
    '# Gas\n'
)

# ===== CELL 123: print =====
replace_in_cell(123,
    'print(f"Неразмеченных: {(mask & df[\'l1\'].isna()).sum()}")',
    'print(f"Unlabeled: {(mask & df[\'l1\'].isna()).sum()}")'
)

# ===== CELL 125: markdown =====
replace_in_cell(125,
    'TEXT люки / кабели / пнд / пэ итд.',
    'TEXT hatches / cables / pnd / pe etc.'
)

# ===== CELL 127: print =====
replace_in_cell(127,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 131: markdown =====
replace_in_cell(131,
    'ТЕКСТ паттерн 1111-ААА-111',
    'TEXT pattern 1111-AAA-111'
)

# ===== CELL 133: markdown =====
replace_in_cell(133,
    'ТЕКСТ паттерн 2186377.187;496579.211',
    'TEXT pattern 2186377.187;496579.211'
)

# ===== CELL 137: markdown =====
replace_in_cell(137,
    'доп. паттерны',
    'additional patterns'
)

# ===== CELL 140: print =====
replace_in_cell(140,
    'print(f"Неразмеченных: {(mask & df[\'l1\'].isna()).sum()}")',
    'print(f"Unlabeled: {(mask & df[\'l1\'].isna()).sum()}")'
)

# ===== CELL 142: markdown =====
replace_in_cell(142,
    'имя деревьев',
    'tree names'
)

# ===== CELL 147: print =====
replace_in_cell(147,
    'print(f"Всего: {mask.sum()}, неразмеченных: {(mask & df[\'l1\'].isna()).sum()}")',
    'print(f"Total: {mask.sum()}, unlabeled: {(mask & df[\'l1\'].isna()).sum()}")'
)

# ===== CELL 149: markdown =====
replace_in_cell(149,
    'ФИО / Ген.директор и т.д.',
    'Full name / Director etc.'
)

# ===== CELL 153: print =====
replace_in_cell(153,
    'print(f"Всего: {mask.sum()}, неразмеченных: {(mask & df[\'l1\'].isna()).sum()}")',
    'print(f"Total: {mask.sum()}, unlabeled: {(mask & df[\'l1\'].isna()).sum()}")'
)

# ===== CELL 156: print =====
replace_in_cell(156,
    'print(f"Всего: {mask.sum()}, неразмеченных: {(mask & df[\'l1\'].isna()).sum()}")',
    'print(f"Total: {mask.sum()}, unlabeled: {(mask & df[\'l1\'].isna()).sum()}")'
)

# ===== CELL 160: markdown =====
replace_in_cell(160,
    'топографические полевые коды (field codes) — сокращения которые геодезисты вводят при съёмке. Расшифровка очевидна:',
    'Topographic field codes — abbreviations surveyors enter during fieldwork. Decoding is straightforward:'
)
replace_in_cell(160,
    'CNT = контур, STR = строение, OGRS/OGRD = ограждение, BRL/BRR = бровка, RST = рельеф, TROPA = тропа, GAZON = газон, ASPH = асфальт, PLITKA = плитка, DER = дерево, KAB = кабель, LEP = ЛЭП, KOLODEC = колодец, TURNIK = турник, KASHELI = качели, LAVKA = лавка, YAMA = яма, BESEDKA = беседка и т.д.',
    'CNT = contour, STR = building, OGRS/OGRD = fence, BRL/BRR = edge, RST = relief, TROPA = path, GAZON = lawn, ASPH = asphalt, PLITKA = pavement, DER = tree, KAB = cable, LEP = power line, KOLODEC = manhole, TURNIK = pull-up bar, KASHELI = swings, LAVKA = bench, YAMA = pit, BESEDKA = gazebo, etc.'
)

# ===== CELL 233: print =====
replace_in_cell(233,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 235: print =====
replace_in_cell(235,
    '| размечено: {total_changed} | осталось: {total_nan}',
    '| labeled: {total_changed} | remaining: {total_nan}'
)

# ===== CELL 256: comments and print strings =====
replace_in_cell(256,
    '# 1. Наш основной паттерн для поиска',
    '# 1. Main search pattern'
)
replace_in_cell(256,
    '# 2. Паттерн для исключения (найдет ПОДЗЕМ.СООР., ПОДЗЕМНОЕ СООРУЖЕНИЕ, ПОДЗ.СООР. и т.д.)',
    '# 2. Exclusion pattern (matches ПОДЗЕМ.СООР., ПОДЗЕМНОЕ СООРУЖЕНИЕ, ПОДЗ.СООР., etc.)'
)
replace_in_cell(256,
    '# 3. Обновленная маска',
    '# 3. Updated mask'
)
replace_in_cell(256,
    '# 4. Выгрузка',
    '# 4. Export'
)
replace_in_cell(256,
    '# Знак ~ исключает совпадения',
    '# ~ operator inverts the mask'
)
replace_in_cell(256,
    'print(f"Файл check_buildings_address.xlsx готов!")',
    'print(f"File check_buildings_address.xlsx is ready!")'
)
replace_in_cell(256,
    'print(f"Найдено уникальных текстов: {len(address_stats)}")',
    'print(f"Unique texts found: {len(address_stats)}")'
)
replace_in_cell(256,
    'print(f"Всего строк попало под паттерн: {mask.sum()}")',
    'print(f"Total rows matched the pattern: {mask.sum()}")'
)
replace_in_cell(256,
    'print("По заданному паттерну не найдено неразмеченных строк.")',
    'print("No unlabeled rows matched the pattern.")'
)

# ===== CELL 328: comments and print =====
replace_in_cell(328,
    '# 1. Оставляем ТОЛЬКО те строки, где текущая разметка не совпадает с эталоном',
    '# 1. Keep ONLY rows where current labels differ from the reference'
)
replace_in_cell(328,
    '# 2. Берем нужные колонки',
    '# 2. Select required columns'
)
replace_in_cell(328,
    '# 3. Удаляем дубликаты, оставляя только уникальные примеры расхождений',
    '# 3. Remove duplicates, keeping only unique mismatch examples'
)
replace_in_cell(328,
    '# 4. Сохраняем в Excel',
    '# 4. Save to Excel'
)
replace_in_cell(328,
    'print(f"Осталось уникальных конфликтов: {len(unique_diffs)}")',
    'print(f"Unique conflicts remaining: {len(unique_diffs)}")'
)

with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('\nAll done!')
