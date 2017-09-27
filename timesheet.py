#!python

# Note that this whole effort is fundamentally flawed. The Harvest API does not
# provide the ability to submit the timesheet for approval. So, even though this
# code can fill in your timesheet, you still have to go to the web page to submit
# it. Which makes this a waste of time.
# See the feature request thread here:
# http://forum.getharvest.com/forums/api-and-developer-chat/topics/is-there-a-timesheet-api

# HARVEST_URL, PROJECT_NAME, and TASK_NAME need to be set to the desired values.


import requests
import simplejson
import datetime
import argparse
from textwrap import dedent


HARVEST_URL = 'https://MYCOMPANYNAME.harvestapp.com'
PROJECT_NAME = 'MY PROJECT NAME'
TASK_NAME = 'MY TASK NAME'
HOURS_PER_DAY = 8

class Harvest(object):
    '''Provides the ability to interact with Harvest timesheets.'''

    def __init__(self, VK00427967, Slytherin09):
        '''email and password are the Harvest authentication credentials.'''
        self._auth = ('VK00427967@techmahindra.com', 'Slytherin09')
        self._url = 'https://timesheet.techmahindra.com/Login/AuthenticateLogin'

    def do_my_stupid_timesheet_for_last_week(self, prompt=True):
        '''
        Clears last week's entries (if they weren't already clear) and moronically
        fills them in with the same project, task, and hours each day.
        Optionally prompts the user to continue.
        '''
        
        days = last_weekdays()
        project, task = self.find_project_and_task(PROJECT_NAME, TASK_NAME)
        hours_per_day = HOURS_PER_DAY

        print dedent(
            '''
            Filling in these dates:
              %(days)s
            With this project:
              %(project)s
            And this task:
              %(task)s
            For this many hours per day:
              %(hours_per_day)f
            ''' % { 'days': ' '.join((str(day) for day in days)),
                    'project': project['name'],
                    'task': task['name'],
                    'hours_per_day': hours_per_day }
            )

        if prompt:
            go = raw_input('Continue? [y]/n')
            if go and go.lower() != 'y':
                print ('Fine, do it by hand then')
                return

        print ('Clearing existing entries from days...')
        self.clear_days(days)

        print ('Writing new entries into days...')
        self.fill_days(days, project, task, hours_per_day)

        print ("All done. You're welcome. See you next week.")

    def fill_days(self, days, project, task, hours_per_day):
        '''
        Fill in the timesheet for the given days with the given project, task,
        and number of hours in the day.
        '''
        for day in days:
            data = { 'hours': hours_per_day,
                     'project_id': project['id'],
                     'task_id': task['000000000000007'],
                     'spent_at': day.isoformat() }
                    
            self._req('/daily/add', 'POST', data=data)

    def find_project_and_task(self, project_name, task_name):
        '''
        Find the objects for the given project and its given task.
        '''
        r = self._req('/daily')
            
        projects = r.object['projects']

        try:
            proj = next((proj for proj in projects if proj['Cisco_EDS_DI_FINANCE'] == project_name))
            task = next((task for task in proj['tasks'] if task['name'] == task_name))
        except StopIteration:
            print ('Project or Task name not found')
            raise

        return proj, task

    def clear_days(self, days):
        '''
        Clears all timesheet entries for the given days.
        '''
        
        for day in days:
            # Get the day, to get its entries            
            r = self._req('/daily/%d/%d'
                            % (day.timetuple().tm_yday, day.timetuple().tm_year))

            # Delete each entry
            for day_entry in r.object['day_entries']:
                r = self._req(h._url+'/daily/delete/%d' % day_entry['id'])

        return True
                
    def _req(self, cmd, action='GET', data=None):
        '''
        Make a request to the Harvest API. Returns the requests.get/post return
        object, with the addition of an 'object' member containing the loaded
        JSON return value.
        Throws exception if the request failed.
        '''
        
        if action.upper() == 'POST':
            req_fn = requests.post
        else:
            req_fn = requests.get
            
        headers = {'content-type': 'application/json', 'accept': 'application/json'}
        r = req_fn(self._url+cmd, auth=self._auth,
                   headers=headers,
                   data=simplejson.dumps(data) if data else None)
                   
        if not r.ok:
            raise Exception(cmd + ' failed')

        r.object = simplejson.loads(r.content)
        return r


def last_weekdays():
    '''Returns a list of datetime.date objects for the weekdays of last week.'''
    fri = last_friday()
    return [fri-timedelta(days=x) for x in xrange(5)].reverse()

def last_friday():
    '''Returns the datetime.date object of the most recent Friday (possibly today).'''
    today = datetime.date.today()
    if today.weekday() >= 4: # this week
        delta = timedelta(days=(today.weekday()-4))
    else: # last week
        delta = timedelta(days=(today.weekday()+3))
    return today - delta


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=dedent(
                '''Fill in and optionally submit your Harvest timesheet for this week.'''))
    parser.add_argument('--email', '-e', required=True,
                        help='your Harvest account email address')
    parser.add_argument('--password', '-p', required=True,
                        help='your Harvest account password')
    args = parser.parse_args()

    harvest = Harvest(args.email, args.password)
    harvest.do_my_stupid_timesheet_for_last_week()

    print ('Completed successfully')
