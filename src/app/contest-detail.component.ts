import { Component, OnInit }                 from '@angular/core';
import { ActivatedRoute, ParamMap, Router }  from '@angular/router';
import { Location }                          from '@angular/common';
import 'rxjs/add/operator/switchMap';

import { ContestDetailService }              from './contest-detail.service';
import { DetailService }                     from './detail.service';

@Component({
    selector: 'contest-detail',
    templateUrl: 'contest-detail.component.html',
    styleUrls: [
        'detail.component.css',
        'contest-detail.component.css',
        'responsive-subhead.css',
        'responsive-sidebar.css'
    ],
    providers: []
})

export class ContestDetailComponent implements OnInit{
    contest: any = [];

    constructor(
        private contestDetailService: ContestDetailService,
        private detailService: DetailService,
        private route: ActivatedRoute,
        private location: Location,
        private router: Router
    ) {}

    ngOnInit(): void {
        this.route.paramMap
            .switchMap((params: ParamMap) => this.contestDetailService.getContestDetails(params.get('id')))
            .subscribe(contest => this.initData(contest));
    }

    initData(contest): void {
        if(!contest.hasOwnProperty("name")){
            this.contest = this.notFound();
        }
        else{
            this.contest = contest;
            // for sidebar
            this.contest.teams = this.detailService.sortTransformObj(contest.teams, "place", true);
            // for meat thermometer
            this.contest.scores = this.detailService.constructScores(contest.teams, false);
            this.contest['barData'] = [
                {
                    desc: 'date',
                    data: this.contest['date_str'],
                    type: 'text'
                },
                {
                    desc: 'prize',
                    data: this.contest['prize'],
                    type: 'dollars'
                },
                {
                    desc: 'location',
                    data: this.contest['location'],
                    type: 'text'
                },
                {
                    desc: 'for',
                    data: this.forIcon(this.contest.is_state_champ, this.contest.prize),
                    type: 'icon'
                }
            ];
        } 
    }

    forIcon(is_champ, prize){
        if(is_champ){
            return "fa-trophy";
        }
        else if(prize > 0){
            return "fa-money";
        }
        else{
            return "fa-smile-o";
        }
    }
    
    notFound(): object {
        let obj = {};
        obj["name"] = "Contest not found";
        obj["state"] = "ks";
        obj["attendance"] = 0;
        obj["barData"] = [
                {
                    desc: "found",
                    data: "nope",
                    type: "text"
                },
                {
                    desc: "found",
                    data: "nope",
                    type: "text"
                },
                {
                    desc: "found",
                    data: "nope",
                    type: "text"
                },
                {
                    desc: "found",
                    data: "nope",
                    type: "text"
                }
            ];
        obj["teams"] = [{"place": "1", "name": "you", "score": "0"}];
        return obj;
    }

    goBack(): void {
        this.location.back();
    }
}
