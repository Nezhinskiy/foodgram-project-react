import styles from './style.module.css'
import { Container, LinkRedirectComponent } from '../index'
import githubImg from '../../images/github-mark-white.png'

const Footer = () => {
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
        <LinkRedirectComponent href='https://github.com/Nezhinskiy' title='Разработал Михаил Нежинский ' image={githubImg} className={styles.footer__brand} />
      </Container>
  </footer>
}

export default Footer