import { Component, OnInit }	from '@angular/core';


@Component({
  selector: 'about-component',
  templateUrl: 'about.component.html',
  styleUrls: [	
  			'detail.component.css',
  			'state-detail.component.css',
                  'about.component.css',
                  'responsive-subhead.css'
             ],
  providers: []
})
export class AboutComponent implements OnInit{
	data: any = {};

	ngOnInit(): void {
      	this.initData();
    	}
    	
    	initData(): void {
		this.data['barData'] = [
			{
			    desc: 'front end',
			    data: 'Angular 2',
			    type: 'text'
			},
			{
			    desc: 'back end',
			    data: 'Firebase',
			    type: 'text'
			},
			{
			    desc: 'lines of code',
			    data: '3000?',
			    type: 'text'
			},
			{
			    desc: 'profit/yr',
			    data: '-50',
			    type: 'dollars'
			}
		];    
    	}
}