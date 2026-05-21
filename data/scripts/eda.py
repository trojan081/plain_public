import ezdxf
import pandas as pd
from pathlib import Path
from typing import Optional

def parse_dxf_to_table(filepath: Path | str) -> Optional[pd.DataFrame]:
    """
    Allocate all the objects to a table
    """
    path = Path(filepath)
    try:
        doc = ezdxf.readfile(path)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

    msp = doc.modelspace()
    data = []
    file_name = path.name

    for entity in msp:
        layer_name = entity.dxf.layer
        entity_type = entity.dxftype()
        
        # Получаем Handle объекта
        handle = entity.dxf.handle
        
        # Получаем имя блока, если это вхождение блока (INSERT)
        block_name = None
        if entity_type == 'INSERT':
            block_name = entity.dxf.name
            
        text_content = None
        if entity_type == 'TEXT':
            text_content = entity.dxf.text
        elif entity_type == 'MTEXT':
            text_content = entity.text
            
        data.append({
            'Source_File': file_name,
            'Handle': handle,
            'Layer': layer_name,
            'Type': entity_type,
            'BlockName': block_name,
            'Text': text_content,
            'l1': None, # Резервируем пустую колонку под классы
            'l2': None  # Резервируем пустую колонку под классы
        })
        
    df = pd.DataFrame(data)
    
    # Защита от пустых файлов
    if df.empty:
        return None
        
    # Жестко фиксируем требуемый формат колонок
    columns_order = ['Source_File', 'Handle', 'Layer', 'Type', 'BlockName', 'Text', 'l1', 'l2']
    df = df[columns_order]
    
    df = df.astype({
        'Source_File': 'string',
        'Handle': 'string',
        'Layer': 'string',
        'Type': 'string',
        'BlockName': 'string',
        'Text': 'string'
    })
        
    return df

def analyze_dataset(df: pd.DataFrame) -> None:
    """
    Dataset statistics
    """
    print('====================================')
    print(f"Total amount of objects: {len(df)}")
    print('====================================')
    print(df['Type'].value_counts().to_string())
    print('====================================')
    print(df['Layer'].value_counts().to_string())
    print('====================================')
    unique_layers = df['Layer'].unique()
    unique_texts = df['Text'].unique() 
    print(f"The number of unique layers: {len(unique_layers)}")
    print(f"The number of unique texts: {len(unique_texts)}")
    
    # Статистика по блокам
    if 'BlockName' in df.columns:
        blocks = df[df['Type'] == 'INSERT']['BlockName'].dropna()
        if not blocks.empty:
            print('====================================')
            print(f"The number of unique blocks: {len(blocks.unique())}")