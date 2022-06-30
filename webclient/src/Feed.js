import React from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import localForage from 'localforage';
import { sourceLink, infoLine, logos } from './utils.js';

class Feed extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			stories: JSON.parse(localStorage.getItem('stories')) || false,
			error: false,
		};
	}

	componentDidMount() {
		fetch('/api')
			.then(res => res.json())
			.then(
				(result) => {
					const updated = !this.state.stories || this.state.stories[0].id !== result.stories[0].id;
					console.log('updated:', updated);

					this.setState({ stories: result.stories });
					localStorage.setItem('stories', JSON.stringify(result.stories));

					if (updated) {
						localForage.clear();
						result.stories.forEach((x, i) => {
							fetch('/api/' + x.id)
								.then(res => res.json())
								.then(result => {
									localForage.setItem(x.id, result.story)
										.then(console.log('preloaded', x.id, x.title));
									this.props.updateCache(x.id, result.story);
								}, error => {}
							);
						});
					}
				},
				(error) => {
					this.setState({ error: true });
				}
			);
	}

	render() {
		const stories = this.state.stories;
		const error = this.state.error;

		return (
			<div className='container'>
				<Helmet>
					<title>Feed - QotNews</title>
					<meta name="robots" content="index" />
				</Helmet>
				{error && <p>Connection error?</p>}
				{stories ?
					<div>
						{stories.map(x =>
							<div className='item' key={x.id}>
								<div className='title'>
									<Link className='link' to={'/' + x.id}>
										<img className='source-logo' src={logos[x.source]} alt='source logo' /> {x.title}
									</Link>

									<span className='source'>
										({sourceLink(x)})
									</span>
								</div>

								{infoLine(x)}
							</div>
						)}
					</div>
				:
					<p>loading...</p>
				}
			</div>
		);
	}
}

export default Feed;
