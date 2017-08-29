import { Component, OnInit }                 from '@angular/core';
import { ActivatedRoute, ParamMap, Router }  from '@angular/router';
import { Location }                          from '@angular/common';
import 'rxjs/add/operator/switchMap';

import { TeamDetailService }                 from './team-detail.service';
import { DetailService }                     from './detail.service';


@Component({
    selector: 'team-detail',
    templateUrl: 'team-detail.component.html',
    styleUrls: [
        'detail.component.css',
        'team-detail.component.css',
        'responsive-subhead.css',
        'responsive-sidebar.css'
    ],
    providers: []
})

export class TeamDetailComponent implements OnInit{
    team: any = {};

    constructor(
        private teamDetailService: TeamDetailService,
        private detailService: DetailService,
        private route: ActivatedRoute,
        private location: Location,
        private router: Router
    ) {}

    ngOnInit(): void {
        this.route.paramMap
            .switchMap((params: ParamMap) => this.teamDetailService.getTeamDetails(params.get('id')))
            .subscribe(team => this.initData(team));
    }

    initData(team): void {
        if(!team.hasOwnProperty("name")){
            this.team = this.notFound();
        }
        else{
            this.team = team;
            // for sidebar
            this.team.contests = this.detailService.sortTransformObj(team.contests, "date_order", false);
            // for meat thermometer
            this.team.scores = this.detailService.constructScores(team.contests, true);
            this.team['barData'] = [
                {
                    desc: 'overall average',
                    data: this.team['overall_avg'],
                    type: 'dec'
                },
                {
                    desc: 'best finish',
                    data: this.team['top_finish'],
                    type: 'text'
                },
                {
                    desc: 'strongest category',
                    data: this.team['strong_cat'],
                    type: 'text'
                },
                {
                    desc: 'top-5 finishes',
                    data: this.team['top_5s'],
                    type: 'int'
                }
            ];
        }
    }

    notFound(): object {
        let obj = {};
        obj["name"] = "Team not found";
        obj["state"] = "ks";
        obj["appearances"] = 0;
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
        obj["contests"] = [{"date_str": "now", "name": "finding this team", "state": "no"}];
        return obj;
    }

    goBack(): void {
        this.location.back();
    }
}
