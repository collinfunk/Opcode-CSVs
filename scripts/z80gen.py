#!/usr/bin/env python3

# Uses https://clrhome.org/table/
# for z80 instruction set

import bs4
import string

FILE = '../z80.html'

class Z80_instruction:
    def __init__(self, dict_val: dict):
        self.dict_val = dict_val
        self.type = dict_val.get('Type', None)
        self.mnemonic = dict_val.get('Mnemonic', None)
        self.opcode = None
        self.bytes = None
        self.cycles = None
        self.flags_affected = None
        self.parse_dict()
        
        if self.opcode is None:
            self.opcode = 'OP_NONE'
        if self.bytes is None:
            self.bytes = '0'
        if self.cycles is None:
            self.cycles = '0'
        if self.flags_affected is None:
            self.flags_affected = 'FLAGS_NONE'
        
    def parse_dict(self):
        self.opcode = self.dict_val.get('Opcode', None)
        self.bytes = self.dict_val.get('Bytes', None)
        self.cycles = self.dict_val.get('Cycles', None)
        carry_affected = self.dict_val.get('C', None)
        negative_affected = self.dict_val.get('N', None)
        parity_affected = self.dict_val.get('P/V', None)
        half_carry_affected = self.dict_val.get('H', None)
        zero_affected = self.dict_val.get('Z', None)
        sign_affected = self.dict_val.get('S', None)
        
        if carry_affected == 'unaffected':
            carry_affected = False
        elif carry_affected == 'affected':
            carry_affected = True
        else:
            carry_affected = None
        if negative_affected == 'unaffected':
            negative_affected = False
        elif negative_affected == 'affected':
            negative_affected = True
        else:
            negative_affected = None
        if parity_affected == 'unaffected':
            parity_affected = False
        elif parity_affected == 'affected':
            parity_affected = True
        else:
            parity_affected = None
        if half_carry_affected == 'unaffected':
            half_carry_affected = False 
        elif half_carry_affected == 'affected':
            half_carry_affected = True
        else:
            half_carry_affected = None
        if zero_affected == 'unaffected':
            zero_affected = False   
        elif zero_affected == 'affected':
            zero_affected = True
        else:
            zero_affected = None
        if sign_affected == 'unaffected':
            sign_affected = False
        elif sign_affected == 'affected':
            sign_affected = True
        else:
            sign_affected = None
        flags_affected = 'FLAGS_'
        if carry_affected is not None:
            flags_affected += 'C' if carry_affected else ''
        if negative_affected is not None:
            flags_affected += 'N' if negative_affected else ''
        if parity_affected is not None:
            flags_affected += 'P' if parity_affected else ''
        if half_carry_affected is not None:
            flags_affected += 'H' if half_carry_affected else ''
        if zero_affected is not None:
            flags_affected += 'Z' if zero_affected else ''
        if sign_affected is not None:
            flags_affected += 'S' if sign_affected else ''
        if flags_affected == 'FLAGS_':
            flags_affected = 'FLAGS_NONE'
        self.flags_affected = flags_affected
        
        if self.type is None and self.mnemonic is not None:
            self.type = 'documented'
        
    def __str__(self):
        # csv format
        # Commas in the mnemonic are wrapped in quotes
        if self.mnemonic is not None and ',' in self.mnemonic:
            self.mnemonic = '"' + self.mnemonic + '"'
        str = f'{self.opcode},{self.type},{self.mnemonic},{self.bytes},{self.cycles},{self.flags_affected}'
        return str
        
    
def main():
    
    soup = bs4.BeautifulSoup(open(FILE), 'html.parser')
    
    td_tags = soup.find_all('td')
    
    instructions = []
    
    for td in td_tags:
        dt_tags = td.find_all('dt')
        dd_tags = td.find_all('dd')
        op_dict = {}
        td_lines = td.text.splitlines()
        mnemonic = td_lines[1].strip() if len(td_lines) > 1 else None
        td_class = td.get('class')
        if td_class is not None:
            op_dict['Type'] = td_class[0]
            
        op_dict['Mnemonic'] = mnemonic
        for dt, dd in zip(dt_tags, dd_tags):
            dict = {}
            op_dict[dt.text.strip()] = dd.text.strip()
        
        instructions.append(Z80_instruction(op_dict))
        
    for instruction in instructions:
        string_val = str(instruction)
        if string_val is not None and string_val != '':
            print(string_val)
        
        
if __name__ == '__main__':
    main()