export function Footer() {
  return (
    <div className="my-10 w-full py-2 px-5 flex flex-col gap-2 items-center justify-center">
      <p className="lg:hidden md:hidden text-center text-xs text-gray-400 dark:text-gray-400">
        I strongly recommend viewing this website on a desktop :)
      </p>
      <p className="text-sm text-center text-gray-500 dark:text-gray-400">
        &copy; {new Date().getFullYear()} 🇪🇸 Built by{" "}
        <a
          href="https://juan.aallende.com"
          target="_blank"
          className="text-blue-500 underline"
          rel="noopener noreferrer"
        >
          Juan
        </a>{" "}
        in Madrid, Spain.
      </p>
    </div>
  );
}
