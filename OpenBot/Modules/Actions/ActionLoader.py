from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import FileManager, OpenLib
from OpenBot.Modules.Actions import Action, ActionFunctions, ActionRequirementsCheckers


functions_args_pattern = {
    # Standard
    'ClearFloor': [[0, 0]],
    'DestroyByVID': [0],
    'DestroyByID': [0],
    'MoveToPosition': [[0, 0], ''],
    'TalkWithNPC': [0, [], ''],
    'ChangeChannel': [0],
    'UseItemOnNPC': [0, 0],

    # Alchemist
    'BuyItemsForAlchemist': [0, ''],
    'ExchangeItemsForAlchemist': [[], 0, ''],
    'ExchangeEnergyFragmentsToCrystal': [0, ''],
    'GetEnergyFromAlchemist': [0, 0, ''],

    # Demon Tower
    'OpenAllSeals': [[0, 0]],
    'UpgradeItemInDemonTower': [[]],
    'ExitDT': [],
    'GoToSeventhFloor': [],
    'FindMapInDT': [[0, 0]],
    'OpenASealInMonument': [[0, 0]],

    # Farmbot
    'ExchangeTrashItemsToEnergyFragments': [],
}
functions_methods = {
    # Standard
    'ClearFloor': ActionFunctions.ClearFloor,
    'DestroyByVID': ActionFunctions.DestroyByVID,
    'DestroyByID': ActionFunctions.DestroyByID,
    'MoveToPosition': ActionFunctions.MoveToPosition,
    'TalkWithNPC': ActionFunctions.TalkWithNPC,
    'ChangeChannel': ActionFunctions.ChangeChannel,
    'UseItemOnNPC': ActionFunctions.UseItemOnNPC,

    # Alchemist 
    'BuyItemsForAlchemist': ActionFunctions.BuyItemsForAlchemist,
    'ExchangeItemsForAlchemist': ActionFunctions.ExchangeItemsForAlchemist,
    'GetEnergyFromAlchemist': ActionFunctions.GetEnergyFromAlchemist,

    # Demon Tower
    'OpenAllSeals': ActionFunctions.OpenAllSeals,
    'UpgradeItemInDemonTower': ActionFunctions.UpgradeItemInDemonTower,
    'ExitDT': ActionFunctions.ExitDT,
    'GoToSeventhFloor': ActionFunctions.GoToSeventhFloor,
    'FindMapInDT': ActionFunctions.FindMapInDT,
    'OpenASealInMonument': ActionFunctions.OpenASealInMonument,

    # Farmbot
    'ExchangeTrashItemsToEnergyFragments': ActionFunctions.ExchangeTrashItemsToEnergyFragments,
}
class ActionLoader:

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

            # Function checking
            if 'function' not in current_action_keys:
                DebugPrint('Function is required to create action dict')
                return False
            
            #DebugPrint('Function name ' + loaded_action['function'])
            function = self.LoadFunction(loaded_action['function'])
            if function is None:
                return False


            # Function args checking
            if 'function_args' in current_action_keys:
                DebugPrint('Function args ' + str(loaded_action['function_args']))
                function_args = self.CheckArgs(loaded_action['function'], loaded_action['function_args'])
                if function_args is None:
                    DebugPrint('function args are none')
                    return False
                elif not function_args:
                    DebugPrint('Function args are empty')

            DebugPrint('Requirements ' + str(loaded_action['requirements']))
            requirements = self.CheckRequirements(loaded_action['requirements'])
            if requirements is None:
                DebugPrint('Requirements are none')
                return False
            elif not requirements:
                DebugPrint('Requirements are empty!')

            
            # Name checking
            try:
                DebugPrint(str(loaded_action['name']))
                name = str(loaded_action['name'])
            except KeyError:
                name = 'None'
                DebugPrint('Name is None')
            # 



            action_dict = {
                'name': name,
                'function': function,
                'function_args': function_args,
                'requirements': requirements
            }
            actions.append(action_dict)
        #DebugPrint(actions)
        return actions

    def LoadFunction(self, function_name):
        DebugPrint(str(function_name) + str(functions_methods.keys()))
        if str(function_name) not in functions_methods.keys():
            DebugPrint('Function name does not exist in function_names pattern')
            return None
        return functions_methods[function_name]
    
    def CheckArgs(self, function_name, function_args_to_check):
        correct_args = functions_args_pattern[function_name]
        
        #DebugPrint(str(function_args_to_check))
        DebugPrint(str(function_name))
        if not len(function_args_to_check) == len( function_args_to_check):
            DebugPrint('Length of args_to_check is different than pattern!')
            return None

        for arg_to_check in range(len(function_args_to_check)):
            DebugPrint(str(function_args_to_check[arg_to_check]))
            DebugPrint(str(correct_args[arg_to_check]))
            if type(function_args_to_check[arg_to_check]) == int:
                function_args_to_check[arg_to_check] = int(function_args_to_check[arg_to_check])
                if not type(correct_args[arg_to_check]) == int:
                    try:
                        function_args_to_check[arg_to_check] = int(function_args_to_check[arg_to_check])
                    except Exception as e:
                        DebugPrint('Requirement data ' + str(function_args_to_check[arg_to_check]) + ' should be int!')
                        DebugPrint(str(e))
                    return None
            
            elif type(function_args_to_check[arg_to_check]) == str:
                if not type(correct_args[arg_to_check]) == str:
                    if type(correct_args[arg_to_check]) == int:
                        try:
                            function_args_to_check[arg_to_check] = int(function_args_to_check[arg_to_check])
                        except Exception as e:
                            DebugPrint('Requirement data ' + str(function_args_to_check[arg_to_check]) + ' should be int!')
                            DebugPrint(str(e))
                        return None
                    else:
                        DebugPrint('['+str(arg_to_check)+'] + This argument should be type str!')
                        return None
            
            elif type(function_args_to_check[arg_to_check]) == bool:
                if not type(correct_args[arg_to_check]) == bool:
                    DebugPrint('['+str(arg_to_check)+'] + This argument should be type bool!')
                    return None

            elif type(function_args_to_check[arg_to_check]) == list:
                #DebugPrint(str(type(correct_args[arg_to_check])))
                DebugPrint(str(function_args_to_check[arg_to_check]))
                if type(correct_args[arg_to_check]) is not list:
                    DebugPrint(str(arg_to_check) + 'This argument should be type list!')
                    return None  

                for arg_in_list in range(len(function_args_to_check[arg_to_check])):
                    try:
                        function_args_to_check[arg_to_check][arg_in_list] = int(function_args_to_check[arg_to_check][arg_in_list])
                    except:
                        pass

                #if len(function_args_to_check[arg_to_check]) != len(correct_args[arg_to_check]):
                #    DebugPrint('Length of args_to_check' + '[' + str(arg_to_check) + ']' + ' is different than pattern!')
                #    return None

            #elif callable(function_args_to_check[arg_to_check])


        if function_name == 'BuyItemsForAlchemist':
            function_args_to_check[1] = self.CheckMap(function_args_to_check[1])
        if function_name == 'GetEnergyFromAlchemist':
            function_args_to_check[2] = self.CheckMap(function_args_to_check[2])               
        if function_name == 'ExchangeEnergyFragmentsToCrystal':
            function_args_to_check[1] = self.CheckMap(function_args_to_check[1])
        return function_args_to_check

    def CheckMap(self, map_name):
        DebugPrint(str(map_name))
        if map_name == 'metin2_first_city':
            return OpenLib.GetPlayerEmpireFirstMap()
        elif map_name == 'metin2_second_city':
            return OpenLib.GetPlayerEmpireSecondMap()
        else:
            return str(map_name)

    def CheckRequirements(self, requirements):
        #DebugPrint(str(requirements))
        for requirement in requirements.keys():
            #DebugPrint(requirement)
            if requirement not in ActionRequirementsCheckers.req_list:
                DebugPrint('Requirement ' + requirement + ' is not in this list' + str(ActionRequirementsCheckers.req_list))
                return None
            
            if requirement == ActionRequirementsCheckers.IS_ON_POSITION:
                DebugPrint(str(requirements[requirement]))
                if type(requirements[requirement]) is not list:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not list')
                    return None
            
                if len(requirements[requirement]) != 2:
                    DebugPrint('Position tuple has diffrent size than expected! Should be 2, there are ' + str(len(requirements[requirement])))
                    return None
                
                for _digit in range(len(requirements[requirement])):
                    try:
                        requirements[requirement][_digit] = int(requirements[requirement][_digit])
                    except Exception as e:
                        DebugPrint('Requirement data ' + str(requirements[requirement][_digit]) + ' should be int!')
                        DebugPrint(str(e))
                        return None

            
            elif requirement == ActionRequirementsCheckers.IS_IN_MAP:
                if type(requirements[requirement]) is not list:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not list')
                    return None

                if not requirements[requirement]:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is empty')
                    return None
                
                for _map in range(len(requirements[requirement])):
                    DebugPrint(str(type(requirements[requirement][_map])))
                    if not type(str(requirements[requirement][_map])) == str:
                        DebugPrint('Requirement data ' + str(requirements[requirement][_map]) + ' should be str!')
                        return None

                    requirements[requirement][_map] = self.CheckMap(requirements[requirement][_map])

            elif requirement == ActionRequirementsCheckers.IS_NEAR_POSITION:
                if type(requirements[requirement]) is not list:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not list')
                    return None

                if not len(requirements[requirement]) > 1 or not len(requirements[requirement]) < 4:
                        DebugPrint('Requirement data length' + str(len(requirements[requirement])) + ' should be between 2-3')


                for _digit in range(len(requirements[requirement])):
                    try:
                        requirements[requirement][_digit] = int(requirements[requirement][_digit])
                    except Exception as e:
                        DebugPrint('Requirement data ' + str(requirements[requirement][_digit]) + ' should be int!')
                        DebugPrint(str(e))
                        return None

            elif requirement == ActionRequirementsCheckers.IS_ABOVE_LVL or requirement == ActionRequirementsCheckers.IS_UNDER_LVL:
                try:
                    requirements[requirement] = int(requirements[requirement])
                except Exception as e:
                    DebugPrint(str(e))
                    return None

                if type(requirements[requirement]) is not int:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not int!')
                    return None

                if requirements[requirement] > 120 or requirements[requirement] < 1:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' should be between 1 and 120')
                    return None

            elif requirement == ActionRequirementsCheckers.IS_NEAR_INSTANCE:
                if type(requirements[requirement]) is not int:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not int!')
                    return None   

            elif requirement == ActionRequirementsCheckers.IS_RACE_NEARLY:
                if type(requirements[requirement]) is not list:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not list!')
                    return None                

                if not requirements[requirement]:
                    DebugPrint('Requirement data cannot be empty!')
                    return None
                
                for race in requirements[requirement]:
                    if not type(race) == int:
                        DebugPrint('Race should be int!')
                        return None
            
            elif requirement == ActionRequirementsCheckers.IS_IN_CHANNEL:
                from OpenBot.Modules import ChannelSwitcher
                if type(requirements[requirement]) is not int:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not int!')
                    return None         
                
                ChannelSwitcher.instance.GetChannels()

                channels_length = len(instance.channels.keys())
                if not channels_length:
                    DebugPrint('Channel switcher did not detect any channel!')
                    return None

                if requirements[requirement] < 0 or requirements[requirement] > channels_length:
                    DebugPrint('Invalid channel number!')
                    return None 
            
            elif requirement == ActionRequirementsCheckers.IS_CHAR_READY_TO_MINE:
                if type(requirements[requirement]) is not int:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not int!')
                    return None   

            elif requirement == ActionRequirementsCheckers.IS_DEAD:
                if type(requirements[requirement]) is not int:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not int!')
                    return None      

            elif requirement == ActionRequirementsCheckers.HAS_ITEM:
                if type(requirements[requirement]) is not int:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not int!')
                    return None  

            elif requirement == ActionRequirementsCheckers.HAS_ITEM_IN_COUNT:
                if type(requirements[requirement]) is not list:
                    DebugPrint('Requirement data ' + str(requirements[requirement]) + ' is not list!')
                    return None  

                if len(requirements[requirement]) > 2 or len(requirements[requirement]) < 2:
                    DebugPrint('Requirement data needs 2 variable, got + ' + str(len(requirements[requirement])))
                    return None
            

        return requirements

    def CheckName(self, name):
        if not type(name) == str:
            DebugPrint('Name is not string!')
            return ''
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