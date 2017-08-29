import { Component, Input } from '@angular/core';

@Component({
    selector: 'data-bar',
    templateUrl: 'data-bar.component.html',
    styleUrls: [ 
        'detail.component.css',
        'responsive-subhead.css'
    ],
    providers: []
})

export class DataBarComponent{
    @Input() objList: Array<object> = [];
    @Input() parent: string = "";
    @Input() context: string = "";
}
