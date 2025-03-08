import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.push('/chat');
  }, []);

  return <div>Redirecting to chat...</div>;
}
