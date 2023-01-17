import axios from "axios";


const baseURL = 'http://localhost:8000/'

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: {
        Authorization: localStorage.getItem('access')
            ? `JWT ${localStorage.getItem('access')}`
            : null,
        'Content-Type': 'application/json',
        accept: 'application/json',
    },
})

axiosInstance.interceptors.response.use(
	(response) => {
		return response;
	},
	async function (error) {
		const originalRequest = error.config;

		if (typeof error.response === 'undefined') {
			alert(
				'A server/network error occurred. ' +
					'Looks like CORS might be the problem. ' +
					'Sorry about this - we will get it fixed shortly.'
			);
			return Promise.reject(error);
		}

		if (
			error.response.status === 401 &&
			originalRequest.url === `${baseURL}api/v1/auth/jwt/refresh/`
		) {
			window.location.href = '/log-in';
			return Promise.reject(error);
		}

		if (
			error.response.data.code === 'token_not_valid' &&
			error.response.status === 401 &&
			error.response.statusText === 'Unauthorized'
		) {
			const refreshToken = localStorage.getItem('refresh');

			if (refreshToken) {
				const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

				// exp date in token is expressed in seconds, while now() returns milliseconds:
				const now = Math.ceil(Date.now() / 1000);
				console.log(tokenParts.exp);

				if (tokenParts.exp > now) {
					return axiosInstance
						.post('api/v1/auth/jwt/refresh/', { refresh: refreshToken })
						.then((response) => {
							localStorage.setItem('access', response.data.access);
							localStorage.setItem('refresh', response.data.refresh);

							axiosInstance.defaults.headers['Authorization'] =
								`JWT ${localStorage.getItem('access')}`
							originalRequest.headers['Authorization'] =
								`JWT ${localStorage.getItem('access')}`;

							return axiosInstance(originalRequest);
						})
						.catch((err) => {
							console.log(err);
						});
				} else {
					console.log('Refresh token is expired', tokenParts.exp, now);
					window.location.href = '/log-in';
				}
			} else {
				console.log('Refresh token not available.');
				window.location.href = '/log-in';
			}
		}

		// specific error handling done elsewhere
		return Promise.reject(error);
	}
);

export default axiosInstance