import random
import pprint
import json
import datetime

# set up the parameters


class ScheduleGenerator():
    def __init__(self, everyone, couples=[], start_year=2022):
        self.everyone = everyone
        self.couples = couples
        self.start_year = start_year
        self.seq_len = len(self.everyone)
        self.all_sequences = []
        self.tmp_list = []
        self.schedule = []

    def get_allowable_matches(self):
        gift_lists = {}
        for p in self.everyone:
            gift_lists[p] = []
            for r in self.everyone:
                if p == r:
                    continue
                elif [p, r] in self.couples:
                    continue
                elif [r, p] in self.couples:
                    continue
                else:
                    gift_lists[p].append(r)

        return gift_lists

    def list_builder(self, allowed, idx):
        # recursive, call generate_all_sequences to drive this
        if idx == self.seq_len:
            if self.tmp_list not in self.all_sequences:
                if len(self.tmp_list) == self.seq_len:
                    self.all_sequences.append(list(self.tmp_list))
            return
        for r in allowed[idx]:
            if not r in self.tmp_list:
                self.tmp_list.append(r)
                self.list_builder(allowed, idx+1)
                self.tmp_list.pop()

    def generate_all_sequences(self, gift_lists):
        rec_list = [*gift_lists.values()]
        for idx in range(len(rec_list)):
            self.list_builder(rec_list, idx)

    def write_out_all_sequences(self, fname="sequence_list.txt"):
        with open(fname, 'w') as fp:
            json.dump(self.all_sequences, fp, indent=2)

    def prune_sequences(self):
        unique_set = [set() for _ in range(len(self.everyone))]
        for s in self.all_sequences:
            skipFlag = False
            for idx, item in enumerate(s):
                if item in unique_set[idx]:
                    skipFlag = True
                    break
            if not skipFlag:
                self.schedule.append(s)
                for idx, item in enumerate(s):
                    unique_set[idx].add(item)

        # randomize for extra fun!
        # constant seed makes sure it doesn't change year to year
        random.seed(42)
        random.shuffle(self.schedule)

    def get_this_years_schedule(self, this_year=None):
        if this_year is None:
            this_year = datetime.datetime.now().year
        offset = (this_year - self.start_year) % len(self.schedule)

        return self.schedule[offset]

    def get_total_schedule(self):
        return self.schedule

    def get_num_years(self):
        return len(self.schedule)

    def get_person_assignment(self, schedule, name):
        return schedule[self.everyone.index(name)]



def main():
    everyone = ['Bob', 'Jill', 'Tim', 'Jane', 'William']
    couples = [
        ['Bob', 'Jill'],
        ['Tim', 'Jane']
    ]
    scheduler = ScheduleGenerator(everyone, couples, 2022)

    gift_lists = scheduler.get_allowable_matches()
    scheduler.generate_all_sequences(gift_lists)
    scheduler.prune_sequences()

    # this year's schedule
    this_years_schedule = scheduler.get_this_years_schedule()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(this_years_schedule)
    print("Schedule will repeat every {} years".format(scheduler.get_num_years()))

    assignments = {}
    for p in everyone:
        assignments[p] = scheduler.get_person_assignment(this_years_schedule, p)

    pp.pprint(assignments)


if __name__ == '__main__':
    main()
