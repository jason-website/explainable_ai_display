pipeline {
  agent any
  triggers {
    GenericTrigger(
            genericVariables: [
                    [key: 'commit', value: '$.commits[0].id'],
                    [key: 'committer', value: '$.commits[0].committer.name'],
                    [key: 'ref', value: '$.ref']
            ],
            token: 'explainable_ai_display',
            causeString: 'Triggered by github webhook on commit $commit to $ref by $committer',
            printContributedVariables: true,
            printPostContent: true,
            silentResponse: true
    )
  }
  environment {
    DOCKERHUB_USR = credentials('DOCKERHUB_USR')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([
                $class                           : 'GitSCM',
                branches                         : [[name: '*/master']],
                doGenerateSubmoduleConfigurations: false
        ])
      }
    }

    stage('Generate The Image') {
      steps {
        sh '''
         set +x
         ./ci/gen-image.sh
         '''
      }
    }

    stage('Push Image To Docker hub') {
      steps {
        sh '''
         set +x
         ./ci/deploy.sh dev
         '''
      }
    }

    stage('Deploy') {
              options {
                  timeout(time: 60, unit: 'SECONDS')
              }

              input {
                  message 'Do you want to deploy?'
                  ok 'Yes, go ahead.'
              }

              steps {
                  sh '''
                  set +x
                  ./ci/deploy.sh
                  '''
              }
            }
}
