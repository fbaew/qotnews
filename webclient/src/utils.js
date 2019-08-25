import React from 'react';
import moment from 'moment';
import { Link } from 'react-router-dom';

export const sourceLink = (story) => {
	const url = story.url || story.link;
	const urlObj = new URL(url);
	const host = urlObj.hostname.replace(/^www\./, '');
	return (<a className='source' href={url}>{host}</a>);
};

export const infoLine = (story) =>
	<div className='info'>
		{story.score} points
		by <a href={story.author_link}>{story.author}</a>
		&#8203; {moment.unix(story.date).fromNow()}
		&#8203; on <a href={story.link}>{story.source}</a> | &#8203;
		<Link className={story.num_comments > 99 ? 'hot' : ''} to={'/' + story.id}>
			{story.num_comments} comment{story.num_comments !== 1 && 's'}
		</Link>
	</div>
;

export const clearStorage = () => {
	const themeSetting = localStorage.getItem('theme');
	localStorage.clear();
	localStorage.setItem('theme', themeSetting);
};
