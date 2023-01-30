import React from 'react'
import styles from './style.module.css'
import cn from 'classnames'

const LinkRedirectComponent = ({ href, title, image, className, activeClassName }) => {
  return <a activeClassName={activeClassName} className={cn(styles.link, className)} href={href} target='_blank'>
    {title}<img src={image} height="25" width="25" />
  </a>
}

export default LinkRedirectComponent

// href
// title
// image
// class