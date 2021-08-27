from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import FileManager, OpenLib
from OpenBot.Modules.Actions import Action, ActionFunctions, ActionRequirementsCheckers


functions_args_pattern = {
'ClearFloor': [(0, 0)],
'Destroy': [0, 0],
'Find': [0],
'MoveToPosition': [(0, 0), ''],
'MoveToVID': [0],
'UsingItemOnInstance': [0, 0],
'OpenAllSeals': [(0, 0)],
'UpgradeDeamonTower': [0],
'GoBuyItemsFromNPC': [[], 0, (0, 0)],#, function
'GetEnergyFromAlchemist': [[], 0, (0, 0)],
'ChangeEnergyToCrystal': (0, (0 ,0), ''),
'TalkWithNPC': [0, (0, 0), [], ''],
'MineOre': [0],#, function
'LookForBlacksmithInDeamonTower': [True, 0],
'FindMapInDT': [(0, 0)],
'OpenASealInMonument':[(0, 0)],
'ExchangeTrashItemsToEnergyFragments': [],
'ChangeChannel': [0],   
}
functions_methods = {
    'ClearFloor': ActionFunctions.ClearFloor,
    'Destroy': ActionFunctions.Destroy,
    'Find': ActionFunctions.Find,
    'MoveToPosition': ActionFunctions.MoveToPosition,
    'MoveToVID': ActionFunctions.MoveToVID,
    'UsingItemOnInstance': ActionFunctions.UsingItemOnInstance,
    'OpenAllSeals': ActionFunctions.OpenAllSeals,
    'UpgradeDeamonTower': ActionFunctions.UpgradeDeamonTower,
    'GoBuyItemsFromNPC': ActionFunctions.GoBuyItemsFromNPC,
    'GetEnergyFromAlchemist': ActionFunctions.GetEnergyFromAlchemist,
    'ChangeEnergyToCrystal': ActionFunctions.ChangeEnergyToCrystal,
    'TalkWithNPC': ActionFunctions.TalkWithNPC,
    'MineOre': ActionFunctions.MineOre,
    'LookForBlacksmithInDeamonTower': ActionFunctions.LookForBlacksmithInDeamonTower,
    'FindMapInDT': ActionFunctions.FindMapInDT,
    'OpenASealInMonument': ActionFunctions.OpenASealInMonument,
    'ExchangeTrashItemsToEnergyFragments': ActionFunctions.ExchangeTrashItemsToEnergyFragments,
    'ChangeChannel': ActionFunctions.ChangeChannel,
}
class ActionLoader:
    def __init__(self):
        pass

    def LoadActionsFromFile(self, file_name):
        json_data = FileManager.LoadActionsDict(file_name)

        cleared_actions = self.ValidateRawActions(json_data)
        DebugPrint(str(cleared_actions))

    def ValidateRawActions(self, raw_actions_dict):
        DebugPrint(str(raw_actions_dict))
        actions = []
        for loaded_action in raw_actions_dict['actions']:
            name = None
            function = None
            function_args = []

            current_action_keys = loaded_action.keys()
            if 'function' not in current_action_keys:
                DebugPrint('Function is required to create action dict')
                return False
            
            #DebugPrint('Function name ' + loaded_action['function'])
            function = self.LoadFunction(loaded_action['function'].decode("cp-1252", "strict"))
            if function is None:
                return False

            if 'function_args' in current_action_keys:
                #DebugPrint('Function args ' + str(loaded_action['function_args']))
                function_args = self.CheckArgs(loaded_action['function'].decode("cp-1252", "strict"), loaded_action['function_args'].encode("cp-1252", "strict"))
                if function_args is None:
                    return False
                elif not function_args:
                    DebugPrint('Function args are empty')

            DebugPrint('Requirements ' + str(loaded_action['requirements'].decode("cp-1252", "strict")))
            requirements = self.CheckRequirements(loaded_action['requirements'].decode("cp-1252", "strict"))
            if requirements is None:
                return False
            elif not requirements:
                DebugPrint('Requirements are empty!')

            name = self.CheckName(loaded_action['name'].decode("cp-1252", "strict"))
            if name is None:
                DebugPrint('Name is None')

            action_dict = {
                'name': name,
                'function': function,
                'function_args': function_args,
                'requirements': requirements
            }
            actions.append(action_dict)
        return actions

    def LoadFunction(self, function_name):
        if function_name not in functions_methods.keys():
            DebugPrint('Function name does not exist in function_names pattern')
            return None
        return functions_methods[function_name]
    
    def CheckArgs(self, function_name, function_args_to_check):
        correct_args = functions_args_pattern[function_name]
        
        if not len(correct_args) == len( function_args_to_check):
            DebugPrint('Length of args_to_check is different than pattern!')
            return None

        for arg_to_check in range(len(function_args_to_check)):
            
            if type(function_args_to_check[arg_to_check]) == int:
                if type(correct_args[arg_to_check]) is not int:
                    DebugPrint('['+str(arg_to_check)+'] + This argument should be type int!')
                    return None
            
            elif type(function_args_to_check[arg_to_check]) == str:
                if type(correct_args[arg_to_check]) is not str:
                    DebugPrint('['+str(arg_to_check)+'] + This argument should be type str!')
                    return None
            
            elif type(function_args_to_check[arg_to_check]) == bool:
                if type(correct_args[arg_to_check]) is not bool:
                    DebugPrint('['+str(arg_to_check)+'] + This argument should be type bool!')
                    return None

            elif type(function_args_to_check[arg_to_check]) == tuple:
                if type(correct_args[arg_to_check]) is not tuple:
                    DebugPrint('['+str(arg_to_check)+'] + This argument should be type tuple!')
                    return None

                if len(function_args_to_check[arg_to_check]) != len(correct_args[arg_to_check]):
                    DebugPrint('Length of args_to_check' + '[' + str(arg_to_check) + ']' + ' is different than pattern!')
                    return None

                for arg_in_tuple in range(len(function_args_to_check[arg_to_check])):
                    if type(correct_args[arg_to_check][arg_in_tuple]) is not int:
                        DebugPrint('function_args_to_check' + '[' + str(arg_to_check) + ']' + '[' + str(arg_in_tuple) + ']' + ' This should be int!')
                        return None

            elif type(function_args_to_check[arg_to_check]) == list:
                if type(correct_args[arg_to_check]) is not list:
                    DebugPrint('['+str(arg_to_check)+'] + This argument should be type list!')
                    return None            

                if len(function_args_to_check[arg_to_check]) != len(correct_args[arg_to_check]):
                    DebugPrint('Length of args_to_check' + '[' + str(arg_to_check) + ']' + ' is different than pattern!')
                    return None

            #elif callable(function_args_to_check[arg_to_check])


        if function_name == 'MoveToPosition':
            if type(function_args_to_check[1]) == str:
                function_args_to_check[1] = self.CheckMap(function_args_to_check[1])
            else:
                return None
                
        return function_args_to_check

    def CheckMap(self, map_name):
        if map_name == 'metin2_first_city':
            return OpenLib.GetPlayerEmpireFirstMap()
        elif map_name == 'metin2_second_city':
            return OpenLib.GetPlayerEmpireSecondMap()
        else:
            return map_name

    def CheckRequirements(self, requirements):
        DebugPrint(str(requirements))
        for requirement in requirements.keys():
            DebugPrint(requirement)
            if requirement not in ActionRequirementsCheckers.req_list:
                DebugPrint('Requirement ' + requirement + ' is not in this list' + str(ActionRequirementsCheckers.req_list))
                return None
            
            if requirement == ActionRequirementsCheckers.IS_ON_POSITION:
                if type(requirements[requirement]) is not list:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not list')
                    return None
            
                if len(requirements[requirement]) != 2:
                    DebugPrint('Position tuple has diffrent size than expected! Should be 2, there are ' + str(len(requirements[requirement])))
                    return None
                
                for number in requirements[requirement]:
                    if type(number) != int:
                        DebugPrint('This should be int! ' +str(number))
                        return None
                

            elif requirement == ActionRequirementsCheckers.IS_IN_MAP:
                if type(requirements[requirement]) is not list:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not list')
                    return None
                if not requirements[requirement]:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is empty')
                    return None
                
                for _map in range(len(requirements[requirement])):
                    if type(requirements[requirement][_map]) is not str:
                        DebugPrint('Requirement data ' + str(requirements[requirement][_map]) + ' should be str!')
                        return None

                    requirements[requirement][_map] = self.CheckMap(requirements[requirement][_map])
        
        return requirements

    def CheckName(self, name):
        if type(name) != str:
            DebugPrint('Name is not string!')
            return None
        return name

    def CheckOnSuccess(self, on_success_list):
        for success_key in on_success_list:
            if success_key not in Action.on_success_keys:
                return False
        return True
    
    def CheckOnFailed(self, on_failed_list):
        for failed_key in on_failed_list:
            if failed_key not in Action.on_success_keys:
                return False
        return True

instance = ActionLoader()