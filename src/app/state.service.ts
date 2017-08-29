import { Injectable }               from '@angular/core';
import { Observable, Subject }      from "rxjs/Rx";
import { AngularFireDatabase, 
         FirebaseListObservable, 
         FirebaseObjectObservable } from "angularfire2/database";

@Injectable()
export class StateService {

	constructor(private db: AngularFireDatabase) { }

	// get data for all states for state listing page
	getStates(): FirebaseListObservable<any[]> {
		return this.db.list('/states');
	}

	// get data associated with a single state for state detail page
	getStateDetails(state_id: string): FirebaseObjectObservable<object> {
		return this.db.object('/states/' + state_id);
	}

	// get basic contests data for a single state for state detail page
	getContestsByState(state_id: string): FirebaseListObservable<any[]>{
		return this.db.list('/contests_simple', {
			query: {
				orderByChild: 'state',
				equalTo: state_id
			}
		});
	}
}