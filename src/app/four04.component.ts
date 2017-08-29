import { Component, OnInit } 				from '@angular/core';
import { ActivatedRoute, ParamMap, Router } 	from '@angular/router';
import { Location }                 		from '@angular/common';
import 'rxjs/add/operator/switchMap';



@Component({
	selector: 'four04',
	templateUrl: 'four04.component.html',
	styleUrls: [
		'four04.component.css',
	],
	providers: []
})

export class Four04Component{
	rules: any = ["Prohibited garnish", 
			  "Pooled sauce",
			  "Foreign object", 
			  "Sculpted meat",
			  "Marked container",
			  "Illegal fuel",
			  "Late entry"];
	rule: string = this.rules[Math.floor(Math.random()*this.rules.length)];

	constructor(
		private route: ActivatedRoute,
		private location: Location,
		private router: Router
	) {}
	
	goBack(): void {
		this.location.back();
	}
}
