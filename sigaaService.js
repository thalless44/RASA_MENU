const { Sigaa } = require('sigaa-api');

const sigaa = new Sigaa({
  url: 'https://sigaa.ifsc.edu.br',
  institution: 'IFSC'
});

const loginAndGetActivities = async (username, password) => {
  try {
    const account = await sigaa.login(username, password);
    const bonds = await account.getActiveBonds();

    const activities = [];
    for (const bond of bonds) {
      if (bond.type !== 'student') continue;

      const courses = await bond.getCourses();
      for (const course of courses) {
        activities.push({
          title: course.title,
          period: course.period,
          schedule: course.schedule
        });
      }
    }

    await account.logoff();
    return activities;
  } catch (error) {
    console.error('Erro ao conectar ao SIGAA:', error);
    return [];
  }
};

module.exports = { loginAndGetActivities };
