import { Injectable }               from '@angular/core';
import { Observable, Subject }      from "rxjs/Rx";
import { AngularFireDatabase, 
         FirebaseListObservable, 
         FirebaseObjectObservable } from "angularfire2/database";

@Injectable()
export class TeamDetailService {
  
	constructor(private db: AngularFireDatabase) { }

	getTeamDetails(team_id: string): FirebaseObjectObservable<object> {
		return this.db.object('/teams/' + team_id);
	}
}