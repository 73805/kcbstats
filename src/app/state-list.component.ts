import { Component, OnInit } 	 from '@angular/core';

import { StateService }        from './state.service';

@Component({
  selector: 'state-list.component',
  templateUrl: 'state-list.component.html',
  styleUrls: [ 'state-list.component.css' ],
  providers: []
})
export class StateListComponent implements OnInit{
	states: any = [];

	constructor(private stateService: StateService) { }

	getStates(): void{
		this.stateService.getStates().subscribe(states => this.states = states);
	}
	ngOnInit(): void {
		this.getStates();
	}
}