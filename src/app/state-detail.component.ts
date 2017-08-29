import { Component, OnInit }                 from '@angular/core';
import { ActivatedRoute, ParamMap, Router }  from '@angular/router';
import { Location }                          from '@angular/common';
import 'rxjs/add/operator/switchMap';

import { StateService }                      from './state.service';
import { DetailService }                     from './detail.service';

@Component({
    selector: 'state-detail',
    templateUrl: 'state-detail.component.html',
    styleUrls: [
        'detail.component.css',
        'state-detail.component.css',
        'responsive-subhead.css'
    ],
    providers: []
})

export class StateDetailComponent implements OnInit{
    contests: any = [];
    state: any = {};
    loaded_contests: boolean = false;

    constructor(
        private stateService: StateService,
        private detailService: DetailService,
        private route: ActivatedRoute,
        private location: Location,
        private router: Router
    ) {}

    ngOnInit(): void {
        // get state related data
        this.route.paramMap
            .switchMap((params: ParamMap) => this.stateService.getStateDetails(params.get('id')))
            .subscribe(state => this.initStateData(state));

        // get contests associated with the state
        this.route.paramMap
            .switchMap((params: ParamMap) => this.stateService.getContestsByState(params.get('id')))
            .subscribe(contests => this.initContestData(contests));
    }

    initStateData(state): void {
        if(!state.hasOwnProperty("fullname")){
            this.state = this.notFound();
        }
        else{
            this.state = state;
            if(this.state["prize_avg"] == "NA"){
                this.state["prize_avg"] = 0;
            }
            this.state["barData"] = [
                {
                    desc: 'region',
                    data: state["region"],
                    type: 'text'
                },
                {
                    desc: 'average prize',
                    data: state["prize_avg"],
                    type: 'dollars'
                },
                {
                    desc: 'home teams',
                    data: state["teams_competed"],
                    type: 'int'
                },
                {
                    desc: 'major month',
                    data: state["hot_month"],
                    type: 'text'
                }
            ];
        }
    }

    initContestData(contests): void {
        this.contests = this.detailService.sortOnKey(contests, "date_order", false);
        this.loaded_contests = true;
    }

    getIcon(is_champ, prize): string{
        if(is_champ){
            return "fa-trophy";
        }else if(prize > 0){
            return "fa-money";
        }else{
            return "fa-smile-o";
        }
    }

    notFound(): object {
        let obj = {fullname: "State Not Found", 
                   barData: [
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
                            ]
                    };
        return obj;
    }

    goBack(): void {
        this.location.back();
    }
}