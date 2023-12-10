import os
import xml.etree.ElementTree as ET

import pandas as pd
from lxml import etree

import config


def find_files_and_configs():
    """Find number of config files and configs."""
    print('Counting config files and configs...')
    
    defs_xml_file = os.path.join(config.data_dir, 'kconfig_defs.xml')
    defs_data = parse_defs_xml(defs_xml_file)
    defs_df = pd.DataFrame(defs_data)

    config_files = []
    for item in defs_df['files']:
        config_files.append(list(item.keys())[0])
    file_count = len(list(set(config_files)))
    config_count = defs_df['kdef_count'].sum()
    print('Total config files {}'.format(file_count))
    print('Total configs {}'.format(config_count))

    usage_xml_file = os.path.join(config.data_dir, 'kconfig_usage.xml')
    usage_data = parse_usage_xml(usage_xml_file)
    usage_df = pd.DataFrame(usage_data)
    kdef_used_count = usage_df.shape[0]
    usage_count = usage_df['usage_count'].sum()
    print('Total config used as macro {}'.format(kdef_used_count))
    print('Total number of usage as macro {}'.format(usage_count))


def parse_defs_xml(xml_file: str):
    parser = etree.XMLParser(encoding='ascii', recover=True)
    tree = etree.parse(xml_file, parser=parser)
    node_KconfigRoot = tree.getroot()
    # data = { 
    #     kdef: {
    #         kdef_count: int,
    #         files: { 
    #             filename: defined_at
    #         }
    #     }
    # }
    data = {}
    for node_file in node_KconfigRoot:
        filename = node_file.attrib['fileName']
        for node_Kconfig in node_file:
            kdef = node_Kconfig.attrib['name']
            node_lineno = node_Kconfig.find('lineno')
            lineno = -1
            if node_lineno is not None:
                lineno = node_lineno.text
            if kdef in data:
                data[kdef]['kdef_count'] += 1
                data[kdef]['files'][filename] = int(lineno)
            else:
                data[kdef] = {'kdef_count': 1, 
                              'files': {filename: int(lineno)}}
    data = {
        'kdef': list(data.keys()),
        'kdef_count': [x['kdef_count'] for x in data.values()],
        'files': [x['files'] for x in data.values()]
    }
    return data


def parse_usage_xml(xml_file: str):
    tree = ET.parse(xml_file)
    node_KconfigRoot = tree.getroot()
    # data = { 
    #     kdef: {
    #         usage_count: int,
    #         file_count: int,
    #         files: { 
    #             filename: [int]
    #         }
    #     }
    # }
    data = {}
    macro_prefixes = ('ENABLE_', 'CONFIG_')
    for node_file in node_KconfigRoot:
        filename = node_file.attrib['fileName']
        for node_Kconfig in node_file:
            macro = node_Kconfig.attrib['name']
            for prefix in macro_prefixes:
                if macro.startswith(prefix):
                    macro = macro[len(prefix) : ]
                    break
            lines = node_Kconfig.iter('line')
            lines = [item.text for item in lines]
            if macro in data:
                data[macro]['usage_count'] += len(lines)
                if filename in data[macro]['files']:
                    data[macro]['files'][filename].extend(lines)
                else:
                    data[macro]['file_count'] += 1
                    data[macro]['files'][filename] = lines
            else:
                data[macro] = {'usage_count': len(lines), 'file_count': 1,
                               'files': {filename: lines}}
    for k, v in data.items():
        for filename, lines in v['files'].items():
            lines = [int(x) for x in lines]
            v['files'][filename] = sorted(lines)
        data[k] = v

    data = {
        'kdef': list(data.keys()),
        'usage_count': [x['usage_count'] for x in data.values()],
        'file_count': [x['file_count'] for x in data.values()],
        'files': [x['files'] for x in data.values()]
    }
    return data


def find_config_types():
    "Count different type attributes of Kconfig."
    print('Counting type attributes of Kconfig...')

    defs_xml_file = os.path.join(config.data_dir, 'kconfig_defs.xml')
    kdef_types = parse_kdef_types(defs_xml_file)
    print(kdef_types)


def parse_kdef_types(xml_file: str):
    parser = etree.XMLParser(encoding='ascii', recover=True)
    tree = etree.parse(xml_file, parser=parser)
    node_KconfigRoot = tree.getroot()
    # data = { 
    #     type: count
    # }
    data = {}
    for node_file in node_KconfigRoot:
        for node_Kconfig in node_file:
            node_type = node_Kconfig.find('type')
            kdef_type = ''
            if node_type is not None:
                kdef_type = node_type.text
            if kdef_type in data:
                data[kdef_type] += 1
            else:
                data[kdef_type] = 1
    return data



if __name__ == "__main__":
    find_files_and_configs()
    find_config_types()
    pass
