from espn_api.football import League

class EspnStrengthIndexClient(League):
    def __init__(self, league_id, year, swid, espn_s2):
        super().__init__(
            league_id=league_id,
            year=year,
            swid=swid,
            espn_s2=espn_s2
       )
        self.current_standings=self._get_current_standings()
        self.ranked_managers=self._get_ranked_managers() 
        self.weekly_scores=[]
        self.strength_index_agg={manager: [0,0] for manager in self.ranked_managers}
        self._get_strength_index()
        self.strength_index_sorted=self._sort_strength_index()
        self.llamas=self._get_llamas()
    
    def _get_current_standings(self):
        return super().standings()
    
    def _get_ranked_managers(self):
        return [self.current_standings[i].owners[0].get('firstName', None) for i in range(10)]


    def _get_strength_index(self): 
        for i in range(15):
            week_scores=[]

            for team in self.current_standings:
                if team.scores[i]==0.0:
                    break
                week_scores.append((team.owners[0].get('firstName', None), team.scores[i]))
                
            if not week_scores:
                break
            week_scores.sort(key=lambda week_score: week_score[1])

            week_si=[]
            for i, week_score in enumerate(week_scores):
                week_si.append((week_score[0], i, 9-i))
                self.strength_index_agg[week_score[0]][0]+=i
                self.strength_index_agg[week_score[0]][1]+=9-i

            self.weekly_scores.append(week_si)

    def _sort_strength_index(self):
        si_list=[(owner, record[0], record[1]) for owner, record in self.strength_index_agg.items()]
        return sorted(si_list, key=lambda team: team[1], reverse=True)
    
    def _get_llamas(self):
        llama_rankings={manager: i for i, manager in enumerate(self.ranked_managers)}
        for i, team in enumerate(self.strength_index_sorted):
            if llama_rankings.get(team[0]) is not None:
                llama_rankings[team[0]] -= i
        return sorted([(team, rank) for team, rank in llama_rankings.items()], key=lambda team: team[1])
                