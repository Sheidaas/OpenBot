from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Actions.ActionLoader import instance as actionLoader
from OpenBot.Modules.Schema.Schema import Schema

SCHEMA_KEYS = {'REQUIREMENTS': 'REQUIREMENTS',
                'OPTIONS': 'OPTIONS',
                'SCHEMA_OPTIONS': 'SCHEMA_OPTIONS',
                'NAME': 'NAME',
                'STAGES': 'STAGES'}

SCHEMA_OPTIONS = {'ITEMS_SLOTS': []}

OPTIONS_KEYS = {'Repeats': 0}

REQUIREMENTS_KEYS = {'MAPS': [], 'LVL': 0}


class SchemaLoader:
    """
        Class has the task validate schema, and decrypting it from json.

        LoadSchema - method using to validate raw_chema from web request.
                    Returning Schema or False if data is invalid.
    """
    def __init__(self):
        self.options = {}
        self.schema_options = {}
        self.requirements = {}
        self.stages = {}


    def LoadSchema(self, raw_schema):
        schema = Schema()
        DebugPrint(str(raw_schema))
        for key in raw_schema.keys():
            if key not in SCHEMA_KEYS.keys():
                DebugPrint(str(key) + ' is not in SCHEMA_KEYS')
                return False
        
        self.options = self.CheckSchemaOptions(raw_schema[SCHEMA_KEYS['OPTIONS']])
        if self.options is False:
            DebugPrint('options are invalid')
            return False
        
        self.stages = self.CheckSchemaStages(raw_schema[SCHEMA_KEYS['STAGES']])
        if self.stages is False:
            DebugPrint('stages are invalid')
            return False

        self.requirements = self.CheckSchemaRequirements(raw_schema[SCHEMA_KEYS['REQUIREMENTS']])
        if self.requirements is False:
            DebugPrint('requirements are invalid')
            return False

        schema.options, schema.stages, schema.requirements, schema.name = self.options, self.stages, self.requirements, raw_schema[SCHEMA_KEYS['NAME']]
        DebugPrint(str(schema.stages))
        return schema 

    def CheckSchemaOptions(self, schema_options):
        # schema_options must be a dict
        if not type(schema_options) == dict:
            DebugPrint('SchemaOptions is not dict')
            return False
        
        for key in schema_options.keys():

            if key not in OPTIONS_KEYS.keys():
                DebugPrint(str(key) + ' is not in OPTIONS_KEYS')
                return False
    
            if type(schema_options[key]) != type(OPTIONS_KEYS[key]):
                DebugPrint(str(key) + ' has different value type than expected')
                return False
        
        return schema_options

    def CheckSchemaNeededOptions(self, schema_options):
        if not type(schema_options) == dict:
            DebugPrint('schema options is not dict')
            return False
        needed_option_keys = SCHEMA_OPTIONS.keys()
        for needed_option in schema_options.keys():
            if needed_option not in needed_option_keys:
                DebugPrint(str(needed_option) + ' is not in needed_options_keys')
                return False

            if not isinstance(type(schema_options[needed_option]), type(SCHEMA_OPTIONS[needed_option])):
                DebugPrint(str(needed_option) + ' type has different than expected')
                return False
        return schema_options

    def FullActionsWithProperty(self, actions):
        new_actions = []
        for action in actions:
            for index, argument in enumerate(action['function_args']):
                if type(argument) == str:
                    if argument.find('OPTION.'):
                        argument = argument.replace('OPTION.', '')
                        if argument in self.schema_options.keys():
                            action['function_args'][index] = self.schema_options[argument]
                        else:
                            DebugPrint(str(argument) + ' is not in schema_options.keys()')

            new_actions.append(action)

        return new_actions

    def CheckSchemaRequirements(self, schema_requirements):
        # schema_requirements must be a dict
        if not type(schema_requirements) == dict:
            DebugPrint('schema_requirements is not dict')
            return False
        
        for key in schema_requirements.keys():

            if key not in REQUIREMENTS_KEYS.keys():
                DebugPrint(str(key) + ' is not in REQUIREMENTS_KEYS')
                return False
    
            if type(schema_requirements[key]) != type(REQUIREMENTS_KEYS[key]):
                DebugPrint(str(key) + ' has different value type than expected')
                return False
        
        return schema_requirements

    def CheckSchemaStages(self, schema_stages):
        # schema_stages must be a dict
        if not type(schema_stages) == dict:
            DebugPrint('schema_stages is not dict')
            return False
        
        # checking if stages have order
        schema_stages_keys = schema_stages.keys()
        for index in range(len(schema_stages_keys)):
            if str(index) not in schema_stages_keys:
                DebugPrint(str(index) + 'is not in schema stages keys')
                return False
            schema_stages[str(index)]['ACTIONS'] = actionLoader.ValidateRawActions({'actions':schema_stages[str(index)]['ACTIONS']})
            schema_stages[str(index)]['ACTIONS'] = self.FullActionsWithProperty(schema_stages[str(index)]['ACTIONS'])
            if not schema_stages[str(index)]['ACTIONS']:
                DebugPrint(str(schema_stages[schema_stages_keys[index]]['ACTIONS']) + ' in stage ' + str(index))
                return False
        return schema_stages

schemaLoader = SchemaLoader()

# DUNGEON SCHEMA
