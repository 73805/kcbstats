import { Component, Input }     from '@angular/core';

import { DetailService }                from './detail.service';

@Component({
    selector: 'waffle-charts',
    templateUrl: 'waffle.component.html',
    styleUrls: [ 'waffle.component.css' ],
    providers: []
})

export class WaffleComponent{
    @Input() scores: object;
    @Input() xAxis: string;
    @Input() context: string;
    categories: any = ["chicken", "ribs", "pork", "brisket"];

    constructor(
        private detailService: DetailService
    ) {}

    getScoreColor(val): string{
        if(!val){
            return "undef";
        }else{
            val = Math.floor(val);
            // all 9
            if(val == 180){
                return "excellent";
            }
            // all 8
            else if(val >= 170){
                return "very-good";
            }
            // all 7
            else if(val >= 160){
                return "above-average";
            }
            // all 6
            else if(val >= 150){
                return "average";
            }
            // below all 6
            else{
                return "below-average";
            }
        }
    }
}