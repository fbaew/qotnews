import React from 'react';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';
import localForage from 'localforage';
import './Style-light.css';
import './Style-dark.css';
import './Style-red.css';
import './fonts/Fonts.css';
import { BackwardDot, ForwardDot } from './utils.js';
import Feed from './Feed.js';
import Article from './Article.js';
import Comments from './Comments.js';
import Search from './Search.js';
import Submit from './Submit.js';
import Results from './Results.js';
import ScrollToTop from './ScrollToTop.js';

class App extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			theme: localStorage.getItem('theme') || '',
		};

		this.cache = {};
	}

	updateCache = (key, value) => {
		this.cache[key] = value;
	}

	light() {
		this.setState({ theme: '' });
		localStorage.setItem('theme', '');
	}

	dark() {
		this.setState({ theme: 'dark' });
		localStorage.setItem('theme', 'dark');
	}

	red() {
		this.setState({ theme: 'red' });
		localStorage.setItem('theme', 'red');
	}

	componentDidMount() {
		if (!this.cache.length) {
			localForage.iterate((value, key) => {
				this.updateCache(key, value);
			});
			console.log('loaded cache from localforage');
		}
	}

	goFullScreen() {
		if ('wakeLock' in navigator) {
			navigator.wakeLock.request('screen');
		}

		document.body.requestFullscreen({ navigationUI: 'hide' }).then(() => {
			window.addEventListener('resize', () => this.forceUpdate());
			this.forceUpdate();
		});
	};

	exitFullScreen() {
		document.exitFullscreen().then(() => {
			this.forceUpdate();
		});
	};

	render() {
		const theme = this.state.theme;
		document.body.style.backgroundColor = theme ? '#000' : '#eeeeee';
		const fullScreenAvailable = document.fullscreenEnabled ||
			document.mozFullscreenEnabled ||
			document.webkitFullscreenEnabled ||
			document.msFullscreenEnabled;

		return (
			<div className={theme}>
				<Router>
					<div className='container menu'>
						<p>
							<Link to='/'>QotNews</Link>

							<span className='theme'><a href='#' onClick={() => this.light()}>Light</a> - <a href='#' onClick={() => this.dark()}>Dark</a> - <a href='#' onClick={() => this.red()}>Red</a></span>
							<br />
							<span className='slogan'>Hacker News, Reddit, Lobsters, and Tildes articles rendered in reader mode.</span>
						</p>
						<Route path='/(|search)' component={Search} />
						<Route path='/(|search)' component={Submit} />
						{fullScreenAvailable &&
							<Route path='/(|search)' render={() => !document.fullscreenElement ?
								<button className='fullscreen' onClick={() => this.goFullScreen()}>Enter Fullscreen</button>
							:
								<button className='fullscreen' onClick={() => this.exitFullScreen()}>Exit Fullscreen</button>
							} />
						}
					</div>

					<Route path='/' exact render={(props) => <Feed {...props} updateCache={this.updateCache} />} />
					<Switch>
						<Route path='/search' component={Results} />
						<Route path='/:id' exact render={(props) => <Article {...props} cache={this.cache} />} />
					</Switch>
					<Route path='/:id/c' exact render={(props) => <Comments {...props} cache={this.cache} />} />

					<BackwardDot />
					<ForwardDot />

					<ScrollToTop />
				</Router>
			</div>
		);
	}
}

export default App;
