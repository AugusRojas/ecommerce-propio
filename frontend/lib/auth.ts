export const getToken = () => (typeof window === 'undefined' ? null : localStorage.getItem('token'))
