import { Component, OnInit } 		from '@angular/core';
import { Router, NavigationEnd } 	from '@angular/router';
import { Location, PopStateEvent } 	from "@angular/common";


@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: [ 'app.component.css' ],
  providers: []
})
export class AppComponent implements OnInit{
	private lastPoppedUrl: string;

	constructor(private router: Router, private location: Location) { }

	ngOnInit() {
		this.location.subscribe((ev:PopStateEvent) => {
			this.lastPoppedUrl = ev.url;
		});
		this.router.events.subscribe((ev) => {
		if (ev instanceof NavigationEnd) {
			if (ev.url == this.lastPoppedUrl)
				this.lastPoppedUrl = undefined;
			else
				window.scrollTo(0, 0);
		}
		});
	}
}