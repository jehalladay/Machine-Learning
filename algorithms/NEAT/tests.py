'''
This file contains the unit tests for the NEAT algorithm. 
'''

import sys
import os
import datetime
import neat

DATA = ''

def main() -> None:
    """runs all the tests"""
    verify_package()

    try_test((1,2,3,4))


def log_test_data(data: str) -> None:
    '''
    Saves all test data to a file along with date and neat version
    '''

    #get current date
    date = str(datetime.datetime.now())

    #open file
    with open('test_log.txt', 'a') as f:
        #write date and version
        f.write(f'''
            NEAT Version: {neat.__version__}
            Test Date:    {date}
            Author:       {neat.__author__}

            {data}
        ''')



def unit_test(Set: int) -> True: #if all tests pass
    """tests for individual functions, only tests the set of tests that is specifically called
    provides print statements that inform the user of which tests fail or pass"""
    assert(type(Set)) == int
    msg = f'Testing set {Set}: no function'
    print(msg)
    global DATA 
    DATA += msg + '\n'
    if Set == 1:
        pass
    elif Set == 2:
        pass
    elif Set == 3:
        pass
    elif Set == 4:
        pass
    return True


def try_test(value: tuple):
    """function runs test functions and handles the raised errors
    takes a tuple input and runs the test that corresponds to the elements in the tuple
    """
    assert(type(value)) == tuple
    global DATA
    msg = ''
    for i in value:
        try: 
            assert unit_test(i) == True
            msg += f'Unit test on set {i} passes\n'
        except AssertionError:
            msg += f'Unit test on set {i} fails\n'
    print(msg)
    DATA += msg


def verify_package() -> bool:
    '''Verifies that the correct neat package has been imported'''
    try:
        assert(neat.__author__ == "James E. Halladay")
        return True
    except AssertionError:
        print('Wrong NEAT library imported')
        return False



if __name__ == '__main__':
    main()
    log_test_data(DATA)